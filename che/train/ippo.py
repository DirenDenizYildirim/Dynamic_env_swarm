"""PureJaxRL-style IPPO on the CHE environment (Milestone 0.5).

One policy, parameters shared across agents (see networks.py DECISION).
Each agent is an independent PPO "sample" receiving the team reward; the
collector scans `step_autoreset` over rollout_len, GAE(lambda) runs over
the time axis, and minibatched clipped-surrogate epochs are jitted end to
end. K updates run inside a single compiled `lax.scan` chunk; the Python
outer loop only handles JSONL metric logging, orbax checkpointing every
`ckpt_interval` updates, and SIGTERM-triggered save-and-exit (spot-instance
interruption is the assumed deployment).
"""

import argparse
import dataclasses
import functools
import hashlib
import json
import signal
import time
from pathlib import Path
from typing import NamedTuple

import distrax
import jax
import jax.numpy as jnp
import optax
import orbax.checkpoint as ocp
from flax.training.train_state import TrainState

from che.env.config import Config, load_config
from che.env.env import N_ACTIONS, reset
from che.train.networks import ActorCritic
from che.train.rollout import batch_rollout, make_random_policy, step_autoreset


class Transition(NamedTuple):
    done: jax.Array  # [n_envs] episode ended at this step
    action: jax.Array  # [n_envs, n_agents]
    value: jax.Array  # [n_envs, n_agents]
    reward: jax.Array  # [n_envs] team reward
    log_prob: jax.Array  # [n_envs, n_agents]
    obs_grid: jax.Array  # [n_envs, n_agents, k, k, 3]
    obs_vec: jax.Array  # [n_envs, n_agents, 4]
    finished_return: jax.Array  # [n_envs] episodic return where done, else 0


def compute_gae(
    rewards: jax.Array,
    values: jax.Array,
    dones: jax.Array,
    last_value: jax.Array,
    *,
    gamma: float,
    gae_lambda: float,
) -> tuple[jax.Array, jax.Array]:
    """GAE(lambda) over the leading time axis (PureJaxRL formulation).

    rewards/dones broadcast against values (e.g. [T, E, 1] vs [T, E, N]);
    dones[t] = True means the episode ended AT step t, so no bootstrapping
    across the t -> t+1 boundary. Returns (advantages, value targets).
    """

    def scan_fn(carry, xs):
        gae, next_value = carry
        reward, value, done = xs
        not_done = 1.0 - done.astype(jnp.float32)
        delta = reward + gamma * next_value * not_done - value
        gae = delta + gamma * gae_lambda * not_done * gae
        return (gae, value), gae

    (_, _), advantages = jax.lax.scan(
        scan_fn,
        (jnp.zeros_like(last_value), last_value),
        (rewards, values, dones),
        reverse=True,
    )
    return advantages, advantages + values


class TrainFns(NamedTuple):
    init: object  # (key) -> runner_state
    chunk: object  # (runner_state, n_updates static) -> (runner_state, metrics)


@functools.lru_cache(maxsize=8)
def make_train_fns(cfg: Config) -> TrainFns:
    """Build (and cache per-config) the jitted init and K-update-chunk fns."""
    ecfg, tcfg = cfg.env, cfg.train
    network = ActorCritic(N_ACTIONS)

    def init_runner(key: jax.Array):
        key, k_net, k_reset = jax.random.split(key, 3)
        k = ecfg.obs_window
        params = network.init(
            k_net,
            jnp.zeros((1, k, k, 3), jnp.float32),
            jnp.zeros((1, 4), jnp.float32),
        )
        tx = optax.chain(
            optax.clip_by_global_norm(tcfg.max_grad_norm),
            optax.adam(tcfg.lr, eps=1e-5),
        )
        train_state = TrainState.create(apply_fn=network.apply, params=params, tx=tx)
        obs, env_states = jax.vmap(reset, in_axes=(0, None))(
            jax.random.split(k_reset, tcfg.n_envs), ecfg
        )
        ep_ret = jnp.zeros((tcfg.n_envs,), jnp.float32)
        return (train_state, env_states, obs, ep_ret, key)

    def _env_step(runner, _):
        train_state, env_states, last_obs, ep_ret, key = runner
        key, k_sample, k_step = jax.random.split(key, 3)
        logits, value = network.apply(
            train_state.params, last_obs["grid"], last_obs["vec"]
        )
        pi = distrax.Categorical(logits=logits)
        action = pi.sample(seed=k_sample)
        log_prob = pi.log_prob(action)
        obs, env_states, reward, done, _info = jax.vmap(
            step_autoreset, in_axes=(0, 0, 0, None)
        )(jax.random.split(k_step, tcfg.n_envs), env_states, action, ecfg)
        ep_ret = ep_ret + reward
        trans = Transition(
            done=done,
            action=action,
            value=value,
            reward=reward,
            log_prob=log_prob,
            obs_grid=last_obs["grid"],
            obs_vec=last_obs["vec"],
            finished_return=jnp.where(done, ep_ret, 0.0),
        )
        ep_ret = jnp.where(done, 0.0, ep_ret)
        return (train_state, env_states, obs, ep_ret, key), trans

    def _loss_fn(params, mb, clip_eps):
        logits, value = network.apply(params, mb["obs_grid"], mb["obs_vec"])
        pi = distrax.Categorical(logits=logits)
        log_prob = pi.log_prob(mb["action"])
        ratio = jnp.exp(log_prob - mb["log_prob"])
        adv = mb["adv"]
        adv = (adv - adv.mean()) / (adv.std() + 1e-8)
        pg_loss = -jnp.minimum(
            ratio * adv,
            jnp.clip(ratio, 1.0 - clip_eps, 1.0 + clip_eps) * adv,
        ).mean()
        v_clipped = mb["value"] + jnp.clip(
            value - mb["value"], -clip_eps, clip_eps
        )
        v_loss = 0.5 * jnp.maximum(
            (value - mb["target"]) ** 2, (v_clipped - mb["target"]) ** 2
        ).mean()
        entropy = pi.entropy().mean()
        total = pg_loss + tcfg.vf_coef * v_loss - tcfg.ent_coef * entropy
        return total, (pg_loss, v_loss, entropy)

    def _update_minibatch(train_state, mb):
        grad_fn = jax.value_and_grad(_loss_fn, has_aux=True)
        (total, aux), grads = grad_fn(train_state.params, mb, tcfg.clip_eps)
        train_state = train_state.apply_gradients(grads=grads)
        return train_state, (total, *aux)

    def _update_epoch(update_state, _):
        train_state, batch, key = update_state
        key, k_perm = jax.random.split(key)
        n = batch["action"].shape[0]
        perm = jax.random.permutation(k_perm, n)
        mb_size = n // tcfg.n_minibatches
        minibatches = jax.tree_util.tree_map(
            lambda x: x[perm][: mb_size * tcfg.n_minibatches].reshape(
                (tcfg.n_minibatches, mb_size, *x.shape[1:])
            ),
            batch,
        )
        train_state, losses = jax.lax.scan(
            _update_minibatch, train_state, minibatches
        )
        return (train_state, batch, key), losses

    def _update_once(runner, _):
        runner, traj = jax.lax.scan(_env_step, runner, None, tcfg.rollout_len)
        train_state, env_states, last_obs, ep_ret, key = runner
        _, last_value = network.apply(
            train_state.params, last_obs["grid"], last_obs["vec"]
        )
        adv, targets = compute_gae(
            traj.reward[:, :, None],
            traj.value,
            traj.done[:, :, None],
            last_value,
            gamma=tcfg.gamma,
            gae_lambda=tcfg.gae_lambda,
        )
        flat = lambda x: x.reshape((-1, *x.shape[3:]))  # noqa: E731
        batch = {
            "obs_grid": flat(traj.obs_grid),
            "obs_vec": flat(traj.obs_vec),
            "action": flat(traj.action),
            "log_prob": flat(traj.log_prob),
            "value": flat(traj.value),
            "adv": flat(adv),
            "target": flat(targets),
        }
        key, k_update = jax.random.split(key)
        (train_state, _, _), losses = jax.lax.scan(
            _update_epoch, (train_state, batch, k_update), None, tcfg.n_epochs
        )
        n_done = traj.done.sum()
        metrics = {
            "mean_return": jnp.where(
                n_done > 0, traj.finished_return.sum() / n_done, jnp.nan
            ),
            "n_episodes": n_done.astype(jnp.int32),
            "total_loss": losses[0].mean(),
            "pg_loss": losses[1].mean(),
            "v_loss": losses[2].mean(),
            "entropy": losses[3].mean(),
        }
        return (train_state, env_states, last_obs, ep_ret, key), metrics

    @functools.partial(jax.jit, static_argnames="n_updates")
    def train_chunk(runner, n_updates: int):
        return jax.lax.scan(_update_once, runner, None, n_updates)

    return TrainFns(init=jax.jit(init_runner), chunk=train_chunk)


# --------------------------------------------------------------- driver


_SIGTERM = {"received": False}


def _sigterm_handler(signum, frame):
    del signum, frame
    _SIGTERM["received"] = True


def config_hash(cfg: Config) -> str:
    return hashlib.sha256(repr(cfg).encode()).hexdigest()[:16]


def _ckpt_manager(ckpt_dir: str | Path) -> ocp.CheckpointManager:
    return ocp.CheckpointManager(
        Path(ckpt_dir).absolute(),
        options=ocp.CheckpointManagerOptions(max_to_keep=3, create=True),
    )


def _save(mngr, runner, update: int):
    train_state = runner[0]
    mngr.save(
        update,
        args=ocp.args.StandardSave(
            {
                "params": train_state.params,
                "opt_state": train_state.opt_state,
                "key": runner[4],
                "update": update,
            }
        ),
    )


def train(
    cfg: Config,
    *,
    n_updates: int,
    seed: int = 0,
    ckpt_dir: str | Path | None = None,
    metrics_path: str | Path | None = None,
    resume: bool = False,
    handle_sigterm: bool = False,
    log_every: int = 10,
):
    """Train IPPO; returns (runner_state, history list of per-update dicts).

    Resume is exact-ish (CLAUDE.md): params/opt_state/PRNG key/update counter
    are restored under a config-hash check; env states start fresh.
    """
    fns = make_train_fns(cfg)
    runner = fns.init(jax.random.PRNGKey(seed))
    start = 0
    mngr = _ckpt_manager(ckpt_dir) if ckpt_dir else None
    if mngr:
        hash_file = Path(ckpt_dir) / "config_hash.txt"
        if resume and mngr.latest_step() is not None:
            if hash_file.exists() and hash_file.read_text() != config_hash(cfg):
                raise ValueError(
                    "checkpoint config hash mismatch — refusing to resume"
                )
            start = mngr.latest_step()
            train_state = runner[0]
            template = {
                "params": train_state.params,
                "opt_state": train_state.opt_state,
                "key": runner[4],
                "update": 0,
            }
            restored = mngr.restore(start, args=ocp.args.StandardRestore(template))
            train_state = train_state.replace(
                params=restored["params"], opt_state=restored["opt_state"]
            )
            runner = (train_state, *runner[1:4], restored["key"])
        else:
            hash_file.parent.mkdir(parents=True, exist_ok=True)
            hash_file.write_text(config_hash(cfg))
    prev_handler = None
    if handle_sigterm:
        _SIGTERM["received"] = False
        prev_handler = signal.signal(signal.SIGTERM, _sigterm_handler)

    history = []
    metrics_file = open(metrics_path, "a") if metrics_path else None
    try:
        update = start
        # Only honor the flag when this call installed the handler —
        # otherwise a SIGTERM caught by an earlier train() in the same
        # process would permanently poison later calls.
        while update < n_updates and not (
            handle_sigterm and _SIGTERM["received"]
        ):
            k = min(cfg.train.ckpt_interval, n_updates - update)
            t0 = time.perf_counter()
            runner, metrics = fns.chunk(runner, k)
            jax.block_until_ready(metrics["total_loss"])
            dt = time.perf_counter() - t0
            for i in range(k):
                row = {
                    name: float(vals[i]) for name, vals in metrics.items()
                }
                row["update"] = update + i + 1
                history.append(row)
                if metrics_file:
                    metrics_file.write(json.dumps(row) + "\n")
            update += k
            if metrics_file:
                metrics_file.flush()
            if update % log_every < k:
                recent = [
                    r["mean_return"]
                    for r in history[-20:]
                    if r["mean_return"] == r["mean_return"]  # drop NaN
                ]
                mean_ret = sum(recent) / len(recent) if recent else float("nan")
                print(
                    f"[ippo] update {update}/{n_updates} "
                    f"return~{mean_ret:.2f} "
                    f"({k * cfg.train.rollout_len * cfg.train.n_envs / dt:,.0f} "
                    "env-steps/s)",
                    flush=True,
                )
            if mngr:
                _save(mngr, runner, update)
        if mngr:
            mngr.wait_until_finished()
    finally:
        if metrics_file:
            metrics_file.close()
        if prev_handler is not None:
            signal.signal(signal.SIGTERM, prev_handler)
    return runner, history


def random_baseline(cfg: Config, *, n_episodes: int = 64, seed: int = 0) -> float:
    """Mean episodic return of the uniform-random policy (the M0.5 bar)."""
    ecfg = cfg.env
    policy = make_random_policy(ecfg.n_agents)
    rewards, _, _ = jax.jit(
        lambda k: batch_rollout(k, ecfg, policy, ecfg.horizon, n_episodes)
    )(jax.random.PRNGKey(seed))
    return float(rewards.sum(axis=1).mean())


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", default="che/configs/debug.yaml")
    p.add_argument("--updates", type=int, default=300)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--ckpt-dir")
    p.add_argument("--metrics", help="JSONL metrics output path")
    p.add_argument("--resume", action="store_true")
    # Scale overrides for the acceptance run (debug-or-slightly-larger).
    p.add_argument("--grid-size", type=int)
    p.add_argument("--n-envs", type=int)
    p.add_argument("--rollout-len", type=int)
    p.add_argument("--baseline", action="store_true",
                   help="print the random-policy baseline and exit")
    args = p.parse_args()
    cfg = load_config(args.config)
    if args.grid_size:
        cfg = dataclasses.replace(
            cfg, env=dataclasses.replace(cfg.env, grid_size=args.grid_size)
        )
    train_overrides = {
        k: v
        for k, v in (
            ("n_envs", args.n_envs),
            ("rollout_len", args.rollout_len),
        )
        if v
    }
    if train_overrides:
        cfg = dataclasses.replace(
            cfg, train=dataclasses.replace(cfg.train, **train_overrides)
        )
    if args.baseline:
        print(f"random baseline: {random_baseline(cfg):.3f}")
        return
    train(
        cfg,
        n_updates=args.updates,
        seed=args.seed,
        ckpt_dir=args.ckpt_dir,
        metrics_path=args.metrics,
        resume=args.resume,
        handle_sigterm=True,
    )


if __name__ == "__main__":
    main()
