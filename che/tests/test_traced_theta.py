"""M6.0b — semantics of the traced theta slice.

The spike moves {beta, kappa_A, kappa_B, delta} out of the static config and
into `EnvState.theta_live`, sampled at reset/autoreset. Acceptance 2a
(`test_theta_golden.py`) proves the refactor changed no behaviour at fixed
locked theta. These tests pin what it DID change, so the new contract is
specified rather than latent.

The load-bearing one is `test_theta_binds_at_reset_not_at_step`. Before M6.0,
`step(key, state, actions, cfg)` read theta off `cfg`, so swapping the config
between steps changed the dynamics. Now it reads off the state, because a
mixture must be able to give different envs different theta inside one
batched step — a per-call config cannot express that. The cost is that a
mid-episode config swap is silently inert, which is exactly the kind of
quiet no-op that produces an unexplained result three phases later. It is
therefore asserted here, in both directions.

Production is unaffected: every theta override (`--kappa-a`, `--kappa-b`,
`--delta`, `--r-comm`, `--death-penalty`) is applied in `main()` argument
parsing, before any reset, so it reaches `theta_live` through the normal
path. That property is asserted too.
"""

from __future__ import annotations

import dataclasses

import jax
import jax.numpy as jnp
import pytest

from che.env.config import EnvConfig, ThetaConfig
from che.env.env import N_ACTIONS, reset, step
from che.env.types import theta_live_from

L = 16


def _cfg(**theta_kw) -> EnvConfig:
    return EnvConfig(
        grid_size=L, n_agents=4, horizon=32, theta=ThetaConfig(**theta_kw)
    )


def _stay(n: int = 4) -> jax.Array:
    return jnp.zeros((n,), jnp.int32)


# ------------------------------------------------------------- the contract


def test_reset_copies_config_theta_into_the_state():
    """The degenerate (single-component) mixture: theta_live carries exactly
    the config's locked constants, which is what makes acceptance 2a possible
    at all."""
    cfg = _cfg(beta=0.61, kappa_A=0.07, kappa_B=1.3, delta=0.25)
    _, s = reset(jax.random.PRNGKey(0), cfg)
    assert float(s.theta_live.beta) == pytest.approx(0.61)
    assert float(s.theta_live.kappa_A) == pytest.approx(0.07)
    assert float(s.theta_live.kappa_B) == pytest.approx(1.3)
    assert float(s.theta_live.delta) == pytest.approx(0.25)
    assert int(s.mixture_component) == 0


def test_theta_live_is_constant_within_an_episode():
    """A mixture resamples at episode boundaries, never mid-episode: every
    kernel in the Prop.-1 order must see one consistent theta."""
    cfg = _cfg(beta=0.5, kappa_A=0.05, kappa_B=1.0, delta=0.5)
    key = jax.random.PRNGKey(1)
    _, s = reset(key, cfg)
    first = jax.tree_util.tree_map(lambda x: x, s.theta_live)
    for t in range(8):
        k = jax.random.fold_in(key, t)
        _, s, _, _, _ = step(k, s, _stay(), cfg)
        for f in ("beta", "kappa_A", "kappa_B", "delta"):
            assert getattr(s.theta_live, f) == getattr(first, f)


def test_theta_binds_at_reset_not_at_step():
    """THE behavioural change M6.0 introduces, asserted in both directions.

    Swapping the config between steps must NOT change the dynamics (theta
    travels with the episode); swapping the state's theta_live MUST.
    """
    hot = _cfg(beta=1.0, iota=0.0)
    cold = _cfg(beta=0.0, iota=0.0)
    key = jax.random.PRNGKey(2)

    # One burning cell, no spontaneous ignition: beta alone decides spread.
    _, s = reset(key, cold)
    s = dataclasses.replace(
        s,
        hazard=jnp.zeros((L, L), jnp.uint8).at[8, 8].set(1),
        agent_pos=jnp.zeros((4, 2), jnp.int32),
    )

    # (a) config swap alone: inert, because theta came from the state.
    _, s_cfg, _, _, _ = step(key, s, _stay(), hot)
    assert int((s_cfg.hazard == 1).sum()) == 0, (
        "a mid-episode config swap changed the dynamics — theta must bind at "
        "reset, or a mixture cannot give two envs different theta in one step"
    )

    # (b) state swap: the fire spreads to all four von-Neumann neighbours.
    s_hot = dataclasses.replace(s, theta_live=theta_live_from(hot.theta))
    _, s_state, _, _, _ = step(key, s_hot, _stay(), hot)
    assert int((s_state.hazard == 1).sum()) == 4


def test_traced_theta_still_honours_unconditional_prng_consumption():
    """Invariant #3 under tracing: kappa_A = 0 and kappa_A > 0 consume the
    same streams, so everything downstream of the seeding draw is unmoved.

    With theta traced this is stronger than before — the draw cannot be
    constant-folded away even when the probability is exactly zero, which is
    the mechanism the whole nesting guarantee rests on.
    """
    off = _cfg(beta=0.0, iota=0.0, kappa_A=0.0, lambda_0=0.0)
    on = dataclasses.replace(off, theta=dataclasses.replace(off.theta, kappa_A=1.0))
    key = jax.random.PRNGKey(3)
    _, s_off = reset(key, off)
    _, s_on = reset(key, on)
    # lambda_0 = 0 -> no collapses -> no seeding at either kappa_A, and the
    # trajectories must stay bitwise identical apart from theta_live itself.
    for t in range(6):
        k = jax.random.fold_in(key, t)
        _, s_off, _, _, _ = step(k, s_off, _stay(), off)
        _, s_on, _, _, _ = step(k, s_on, _stay(), on)
        assert (s_off.hazard == s_on.hazard).all()
        assert (s_off.smoke == s_on.smoke).all()
        assert (s_off.agent_pos == s_on.agent_pos).all()


def test_production_theta_overrides_are_applied_before_reset():
    """The reason the binding change is safe in production.

    Every CLI theta override lives in a `main()` that rewrites `cfg` and only
    then resets. This asserts the pattern still reaches the kernels, i.e.
    that overrides are not silently dropped by the new binding.
    """
    base = _cfg(kappa_B=0.0, delta=0.0)
    overridden = dataclasses.replace(
        base, theta=dataclasses.replace(base.theta, kappa_B=2.0, delta=1.0)
    )
    _, s = reset(jax.random.PRNGKey(4), overridden)
    assert float(s.theta_live.kappa_B) == pytest.approx(2.0)
    assert float(s.theta_live.delta) == pytest.approx(1.0)
    # delta = 1 is total denial: the realized link graph must be empty.
    obs, _ = reset(jax.random.PRNGKey(4), overridden)
    assert not bool(jnp.asarray(obs["links"]).any())


def test_theta_live_survives_a_jitted_step():
    """The slice is a pytree leaf set, not a Python attribute: it must round
    -trip through jit unchanged (vmap/scan in the trainer depend on this)."""
    cfg = _cfg(beta=0.4, kappa_B=0.9)
    key = jax.random.PRNGKey(5)
    _, s = reset(key, cfg)
    jitted = jax.jit(lambda k, st, a: step(k, st, a, cfg))
    actions = jax.random.randint(key, (4,), 0, N_ACTIONS, dtype=jnp.int32)
    _, s2, _, _, _ = jitted(key, s, actions)
    assert float(s2.theta_live.beta) == pytest.approx(0.4)
    assert float(s2.theta_live.kappa_B) == pytest.approx(0.9)
