"""M0.1 scaffold tests: configs load, EnvState builds with declared dtypes."""

from pathlib import Path

import chex
import jax
import jax.numpy as jnp

from che.env.config import Config, ThetaConfig, load_config
from che.env.types import BURNT, FUEL, INTACT, EnvState, zeros_state

CONFIG_DIR = Path(__file__).resolve().parent.parent / "configs"


def test_debug_config_loads():
    cfg = load_config(CONFIG_DIR / "debug.yaml")
    assert isinstance(cfg, Config)
    assert cfg.env.grid_size == 16
    assert cfg.env.n_agents == 4
    assert cfg.train.n_envs == 2
    assert cfg.train.pop_size == 2
    assert cfg.env.theta.kappa_A == 0.0


def test_reference_config_loads():
    cfg = load_config(CONFIG_DIR / "reference.yaml")
    assert cfg.env.grid_size == 64
    assert cfg.env.n_agents == 12
    assert cfg.train.n_envs == 1024
    assert cfg.train.pop_size == 12


def test_configs_are_hashable_static_args():
    # Frozen dataclasses must be usable as jit static arguments.
    cfg = load_config(CONFIG_DIR / "debug.yaml")
    assert hash(cfg) == hash(load_config(CONFIG_DIR / "debug.yaml"))
    assert ThetaConfig() == ThetaConfig()


def test_zeros_state_shapes_and_dtypes():
    cfg = load_config(CONFIG_DIR / "debug.yaml")
    ll, n = cfg.env.grid_size, cfg.env.n_agents
    state = zeros_state(ll, n, jax.random.PRNGKey(0))
    assert isinstance(state, EnvState)
    chex.assert_shape(state.agent_pos, (n, 2))
    chex.assert_shape(state.agent_alive, (n,))
    chex.assert_shape(state.food, (ll, ll))
    chex.assert_shape(state.hazard, (ll, ll))
    chex.assert_shape(state.smoke, (ll, ll))
    chex.assert_shape(state.structure, (ll, ll))
    chex.assert_type(state.agent_pos, jnp.int32)
    chex.assert_type(state.agent_alive, jnp.bool_)
    chex.assert_type(state.food, jnp.uint8)
    chex.assert_type(state.hazard, jnp.uint8)
    chex.assert_type(state.smoke, jnp.float32)
    chex.assert_type(state.structure, jnp.uint8)
    chex.assert_type(state.t, jnp.int32)
    assert (state.hazard == FUEL).all()
    assert (state.structure == INTACT).all()
    assert FUEL < BURNT  # coding sanity


def test_envstate_is_pytree():
    state = zeros_state(8, 2, jax.random.PRNGKey(0))
    leaves = jax.tree_util.tree_leaves(state)
    assert len(leaves) == 10  # M1.4 added the two episode death counters
    # A mapped identity must preserve structure (chex.dataclass registers
    # EnvState as a pytree; vmap/scan rely on this).
    state2 = jax.tree_util.tree_map(lambda x: x, state)
    assert isinstance(state2, EnvState)
