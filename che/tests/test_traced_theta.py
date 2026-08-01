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

from che.env.config import (
    EnvConfig,
    MixtureComponent,
    MixtureConfig,
    ThetaConfig,
    load_config,
)
from che.env.env import N_ACTIONS, reset, step
from che.env.types import theta_live_from
from che.train.rollout import step_autoreset

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


# ------------------------------------------------------- M6.0c: the mixture


def _mix(*comps) -> MixtureConfig:
    return MixtureConfig(components=tuple(comps))


def _mixture_cfg(*comps, **theta_kw) -> EnvConfig:
    return dataclasses.replace(_cfg(**theta_kw), mixture=_mix(*comps))


def test_component_is_a_patch_on_the_base_theta():
    """Unset component fields inherit cfg.theta — the point being that
    locked constants stay in one place instead of being restated per
    component, where they could silently drift apart."""
    cfg = _mixture_cfg(
        MixtureComponent(name="a_off", weight=1.0, kappa_A=0.0),
        beta=0.49,
        kappa_A=0.06,
        kappa_B=1.0,
        delta=1.0,
    )
    _, s = reset(jax.random.PRNGKey(0), cfg)
    assert float(s.theta_live.kappa_A) == pytest.approx(0.0)  # patched
    assert float(s.theta_live.beta) == pytest.approx(0.49)  # inherited
    assert float(s.theta_live.kappa_B) == pytest.approx(1.0)  # inherited
    assert float(s.theta_live.delta) == pytest.approx(1.0)  # inherited


def test_realized_mixture_ratio_matches_weights():
    """Spike acceptance 2d, at CPU scale: the draw must actually realize the
    declared distribution, not merely accept it."""
    cfg = _mixture_cfg(
        MixtureComponent(name="pillar", weight=0.25, kappa_A=0.0, kappa_B=0.0),
        MixtureComponent(name="joint", weight=0.75),
        kappa_A=0.06,
        kappa_B=1.0,
    )
    n = 2000
    keys = jax.random.split(jax.random.PRNGKey(7), n)
    comps = jax.vmap(lambda k: reset(k, cfg)[1].mixture_component)(keys)
    frac_joint = float((comps == 1).mean())
    # ~2.5 sd of a Binomial(2000, 0.75) proportion is ~0.024.
    assert abs(frac_joint - 0.75) < 0.03, f"realized {frac_joint:.3f} vs 0.75"
    # And the drawn theta tracks the component, not just the label.
    kb = jax.vmap(lambda k: reset(k, cfg)[1].theta_live.kappa_B)(keys)
    assert bool(jnp.all((comps == 1) == (kb == 1.0)))


def test_zero_weight_component_is_never_drawn():
    cfg = _mixture_cfg(
        MixtureComponent(name="never", weight=0.0, beta=0.99),
        MixtureComponent(name="always", weight=1.0, beta=0.11),
    )
    keys = jax.random.split(jax.random.PRNGKey(11), 256)
    betas = jax.vmap(lambda k: reset(k, cfg)[1].theta_live.beta)(keys)
    assert bool(jnp.all(betas == jnp.float32(0.11)))


def test_autoreset_resamples_the_component():
    """The mixture draws per EPISODE, so the boundary is where it must move —
    this is the path the Phase-6 trainer actually runs."""
    cfg = dataclasses.replace(
        _mixture_cfg(
            MixtureComponent(name="lo", weight=1.0, beta=0.0),
            MixtureComponent(name="hi", weight=1.0, beta=1.0),
        ),
        horizon=2,  # done fires every other step
    )
    key = jax.random.PRNGKey(13)
    _, s = reset(key, cfg)
    seen, dones = set(), 0
    for t in range(60):
        k = jax.random.fold_in(key, t)
        _, s, _, done, _ = step_autoreset(k, s, _stay(), cfg)
        seen.add(int(s.mixture_component))
        dones += int(done)
    assert dones > 0, "horizon=2 should have produced episode boundaries"
    assert seen == {0, 1}, f"component never varied across resets: {seen}"


def test_info_reports_the_stepping_episodes_component():
    """Under autoreset the returned state may already be a fresh draw while
    `info` describes the episode that just ended — the same numerator/
    denominator discipline the M4.4 and M5.0 channels follow."""
    cfg = dataclasses.replace(
        _mixture_cfg(
            MixtureComponent(name="lo", weight=1.0, beta=0.0),
            MixtureComponent(name="hi", weight=1.0, beta=1.0),
        ),
        horizon=1,  # every step is a boundary
    )
    key = jax.random.PRNGKey(17)
    _, s = reset(key, cfg)
    for t in range(20):
        before = int(s.mixture_component)
        k = jax.random.fold_in(key, t)
        _, s, _, done, info = step_autoreset(k, s, _stay(), cfg)
        assert bool(done)
        assert int(info["mixture_component"]) == before, (
            "info must describe the ending episode, not the fresh draw"
        )


def test_empty_mixture_is_exactly_the_config_theta():
    """The degenerate case is a real single-component mixture, not a bypass:
    it still draws (invariant #3) and still lands on cfg.theta."""
    plain = _cfg(beta=0.37, kappa_A=0.02, kappa_B=0.5, delta=0.25)
    assert plain.mixture.is_empty
    _, s = reset(jax.random.PRNGKey(19), plain)
    for f in ("beta", "kappa_A", "kappa_B", "delta"):
        assert getattr(s.theta_live, f) == pytest.approx(getattr(plain.theta, f))
    assert int(s.mixture_component) == 0


def test_mixture_spec_validation_and_yaml_round_trip(tmp_path):
    with pytest.raises(ValueError, match="duplicate"):
        _mix(
            MixtureComponent(name="x", weight=1.0),
            MixtureComponent(name="x", weight=1.0),
        )
    with pytest.raises(ValueError, match="negative weight"):
        MixtureComponent(name="x", weight=-0.5)
    with pytest.raises(ValueError, match="sum to zero"):
        _mix(MixtureComponent(name="x", weight=0.0))

    path = tmp_path / "mix.yaml"
    path.write_text(
        "env:\n  grid_size: 16\n  n_agents: 4\n"
        "theta:\n  beta: 0.49\n  kappa_A: 0.06\n  kappa_B: 1.0\n"
        "mixture:\n  components:\n"
        "    - {name: a_only, weight: 0.5, kappa_B: 0.0}\n"
        "    - {name: joint, weight: 0.5}\n"
    )
    cfg = load_config(path)
    assert [c.name for c in cfg.env.mixture.components] == ["a_only", "joint"]
    assert cfg.env.mixture.components[0].kappa_B == 0.0
    assert cfg.env.mixture.components[1].kappa_B is None  # inherits
    with pytest.raises(TypeError):  # typo protection, as everywhere else
        MixtureComponent(name="x", weight=1.0, kappa_C=1.0)


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
