"""Batched episode rollouts: lax.scan over time, vmap over envs.

Phase-0 scope: fixed-length rollouts (no auto-reset; that arrives with the
IPPO collector in M0.5). `policy_fn(key, obs) -> actions` is closed over, so
jit callers should treat `cfg` and `policy_fn` as static.
"""

from collections.abc import Callable

import jax
import jax.numpy as jnp

from che.env.config import EnvConfig
from che.env.env import N_ACTIONS, reset, step

PolicyFn = Callable[[jax.Array, dict[str, jax.Array]], jax.Array]


def make_random_policy(n_agents: int) -> PolicyFn:
    """Uniform-random discrete policy (the Phase-0 baseline)."""

    def policy(key: jax.Array, obs: dict[str, jax.Array]) -> jax.Array:
        del obs
        return jax.random.randint(key, (n_agents,), 0, N_ACTIONS, dtype=jnp.int32)

    return policy


def step_autoreset(
    key: jax.Array, state, actions: jax.Array, cfg: EnvConfig
):
    """Env step that resets when done (the IPPO collector's transition).

    Returns (obs, state', reward, done, info) where `done`, `reward`, and
    `info` describe the *ending* episode while `obs`/`state'` are already
    from the fresh reset when done is True. The reset branch is computed
    unconditionally (invariant #3: key consumption never depends on data).
    """
    k_step, k_reset = jax.random.split(key)
    obs, state_new, reward, done, info = step(k_step, state, actions, cfg)
    obs_r, state_r = reset(k_reset, cfg)
    pick = lambda a, b: jnp.where(done, b, a)  # noqa: E731
    state_out = jax.tree_util.tree_map(pick, state_new, state_r)
    obs_out = jax.tree_util.tree_map(pick, obs, obs_r)
    return obs_out, state_out, reward, done, info


def rollout_episode(
    key: jax.Array, cfg: EnvConfig, policy_fn: PolicyFn, n_steps: int
):
    """One episode of `n_steps` env steps from a fresh reset.

    Returns (rewards [T], dones [T], infos {name: [T]}).
    """
    key, k_reset = jax.random.split(key)
    obs0, state0 = reset(k_reset, cfg)

    def body(carry, _):
        key, obs, state = carry
        key, k_act, k_step = jax.random.split(key, 3)
        actions = policy_fn(k_act, obs)
        obs_new, state_new, reward, done, info = step(k_step, state, actions, cfg)
        return (key, obs_new, state_new), (reward, done, info)

    _, (rewards, dones, infos) = jax.lax.scan(
        body, (key, obs0, state0), None, length=n_steps
    )
    return rewards, dones, infos


def batch_rollout(
    key: jax.Array, cfg: EnvConfig, policy_fn: PolicyFn, n_steps: int, n_envs: int
):
    """vmap of rollout_episode over `n_envs` independent keys.

    Returns (rewards [n_envs, T], dones [n_envs, T], infos {name: [n_envs, T]}).
    """
    keys = jax.random.split(key, n_envs)
    return jax.vmap(lambda k: rollout_episode(k, cfg, policy_fn, n_steps))(keys)
