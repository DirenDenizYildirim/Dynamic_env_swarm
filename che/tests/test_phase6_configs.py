"""M6.1 — the Phase-6 protocol configs, checked against the registered design.

`che/scripts/make_phase6_configs.py` emits ten configs whose mixture weights
carry real arithmetic (c − p, 1 − 2c + p). The files are committed so they are
explicit and reviewable; these tests re-derive them so they are also correct.

The load-bearing one is `test_no_training_config_carries_the_held_out_beta`.
theta* sits at beta = 0.49 (`beta_holdout`), and Γ is meaningful only if neither
protocol trains there. That was a comment in `locks.yaml`; a comment is
inherited by memory, and this project's whole locks apparatus exists because
memory is not a mechanism.
"""

from __future__ import annotations

from pathlib import Path

import jax
import jax.numpy as jnp
import pytest

from che.env.config import MAX_MIXTURE_COMPONENTS, load_config
from che.env.env import reset
from che.scripts.make_phase6_configs import PLAN, render

REPO_ROOT = Path(__file__).resolve().parents[2]
HELD_OUT_BETA = 0.49
TRAIN_BETAS = (0.43, 0.70)
NAMES = [name for name, _, _ in PLAN]


def _cfg(name: str):
    return load_config(REPO_ROOT / "che" / "configs" / f"{name}.yaml").env


# ------------------------------------------------- the committed files agree


@pytest.mark.parametrize("name,comps,purpose", PLAN, ids=NAMES)
def test_committed_config_matches_the_generator(name, comps, purpose):
    """No drift between the arithmetic and the artifact. Hand-editing a
    generated config is how a sweep ends up silently unbalanced."""
    on_disk = (REPO_ROOT / "che" / "configs" / f"{name}.yaml").read_text()
    assert on_disk == render(name, comps, purpose), (
        f"{name}.yaml differs from the generator. Re-run "
        "`uv run python -m che.scripts.make_phase6_configs` and commit, or fix "
        "the generator — do not hand-edit the config."
    )


# ------------------------------------------------------------- the trap test


@pytest.mark.parametrize("name", NAMES)
def test_no_training_config_carries_the_held_out_beta(name):
    """θ\\*'s severity must appear in NO training config, base or component.

    Training on β = 0.49 would put θ\\*'s severity into the training
    distribution and destroy the held-out property Γ depends on — a silent
    result-invalidating error, since nothing else would fail.
    """
    cfg = _cfg(name)
    assert cfg.theta.beta != pytest.approx(HELD_OUT_BETA), (
        f"{name}: base beta is the HELD-OUT severity"
    )
    for c in cfg.mixture.components:
        assert c.beta is None or c.beta != pytest.approx(HELD_OUT_BETA), (
            f"{name}: component {c.name!r} trains at the held-out severity "
            f"{HELD_OUT_BETA}. Gamma(theta*) is only meaningful if neither "
            "protocol trained there."
        )


@pytest.mark.parametrize("name", NAMES)
def test_components_use_only_locked_values(name):
    """Every component is built from locked constants — elements are either
    off or at their locked strength, and severities are training severities."""
    for c in _cfg(name).mixture.components:
        assert c.beta in [pytest.approx(b) for b in TRAIN_BETAS], (
            f"{name}/{c.name}: beta {c.beta} is not a training severity"
        )
        assert c.kappa_A in (pytest.approx(0.0), pytest.approx(0.06))
        assert c.kappa_B in (pytest.approx(0.0), pytest.approx(1.0))
        assert c.delta in (pytest.approx(0.0), pytest.approx(1.0))


@pytest.mark.parametrize("name", NAMES)
def test_weights_are_a_normalized_distribution(name):
    comps = _cfg(name).mixture.components
    assert 0 < len(comps) <= MAX_MIXTURE_COMPONENTS
    total = sum(c.weight for c in comps)
    # Weights are written to 6 dp for readability and NORMALIZED at sample
    # time (`env._mixture_table`), so they need not sum to 1 exactly — ISO's
    # 1/6 cells sum to 1.000002. The tolerance is the rounding, not slack:
    # a real imbalance shows up in the realized-draw test below, which
    # compares against binomial noise.
    assert total == pytest.approx(1.0, abs=1e-5), f"{name}: weights sum {total}"
    assert all(c.weight >= 0.0 for c in comps)


# --------------------------------------------- the design's own arithmetic


def _marginals(name: str) -> dict:
    comps = _cfg(name).mixture.components
    tot = sum(c.weight for c in comps)
    f = lambda pred: sum(c.weight for c in comps if pred(c)) / tot  # noqa: E731
    return {
        "A": f(lambda c: c.kappa_A > 0),
        "B": f(lambda c: c.kappa_B > 0),
        "co": f(lambda c: c.kappa_A > 0 and c.kappa_B > 0),
        "none": f(lambda c: c.kappa_A == 0 and c.kappa_B == 0 and c.delta == 0),
    }


@pytest.mark.parametrize(
    "name,c,p",
    [(f"p6_sweep_c50_p{int(p * 1000):03d}", 0.5, p)
     for p in (0.0, 0.125, 0.25, 0.375, 0.5)]
    + [(f"p6_ident_c40_p{int(p * 1000):03d}", 0.4, p)
       for p in (0.0, 0.2, 0.4)],
)
def test_sweep_realizes_its_design(name, c, p):
    """Marginal fixed at c, co-occurrence = p, and the no-element share at
    1 − 2c + p — the confound v2 §2 reports rather than hides."""
    m = _marginals(name)
    assert m["A"] == pytest.approx(c), f"{name}: A marginal {m['A']} != {c}"
    assert m["B"] == pytest.approx(c)
    assert m["co"] == pytest.approx(p), f"{name}: co-occurrence {m['co']} != {p}"
    assert m["none"] == pytest.approx(1 - 2 * c + p)


def test_endpoints_are_the_registered_contrast():
    """ISO sees every element only in isolation; JOINT sees them co-active.
    The pair is deliberately unmatched in marginal — that is how the founding
    registration defines it (v2 §1)."""
    iso = _marginals("p6_iso")
    assert iso["co"] == pytest.approx(0.0), "ISO must never co-activate"
    assert iso["A"] == pytest.approx(1 / 3) and iso["B"] == pytest.approx(1 / 3)
    joint = _marginals("p6_joint")
    assert joint["A"] == pytest.approx(1.0) and joint["B"] == pytest.approx(1.0)
    assert joint["co"] == pytest.approx(1.0)
    # And the delta element: ISO must carry it in isolation, JOINT co-active.
    assert any(c.delta > 0 and c.kappa_A == 0 and c.kappa_B == 0
               for c in _cfg("p6_iso").mixture.components)
    assert all(c.delta > 0 for c in _cfg("p6_joint").mixture.components)


# ------------------------------------------------ realized draw, end to end


@pytest.mark.parametrize("name", ["p6_iso", "p6_sweep_c50_p250"])
def test_realized_draw_matches_declared_weights(name):
    """The declared distribution must actually be what reset() samples —
    the audit acceptance 2d asked for, now at 6 and 8 components."""
    cfg = _cfg(name)
    comps = cfg.mixture.components
    n = 4000
    keys = jax.random.split(jax.random.PRNGKey(3), n)
    drawn = jax.vmap(lambda k: reset(k, cfg)[1].mixture_component)(keys)
    for i, c in enumerate(comps):
        realized = float((drawn == i).mean())
        # ~3.5 sd of a Binomial(n, w) proportion, floored for tiny weights.
        tol = max(3.5 * (c.weight * (1 - c.weight) / n) ** 0.5, 0.004)
        assert abs(realized - c.weight) < tol, (
            f"{name}/{c.name}: realized {realized:.4f} vs declared {c.weight}"
        )


def test_zero_weight_components_are_kept_and_never_drawn():
    """Kept so component INDICES are stable across sweep points — mixture_w2
    must mean the same component at every p, or the per-component audit is
    unreadable. Kept, but never sampled."""
    cfg = _cfg("p6_sweep_c50_p000")
    zeros = [i for i, c in enumerate(cfg.mixture.components) if c.weight == 0.0]
    assert zeros, "expected zero-weight cells at p = 0"
    keys = jax.random.split(jax.random.PRNGKey(5), 1000)
    drawn = jax.vmap(lambda k: reset(k, cfg)[1].mixture_component)(keys)
    for i in zeros:
        assert not bool(jnp.any(drawn == i)), f"component {i} has weight 0"
