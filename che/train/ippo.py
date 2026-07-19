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
from che.env.observation import N_PLANES
from che.train.networks import ActorCritic
from che.train.rollout import batch_rollout, make_random_policy, step_autoreset


class Transition(NamedTuple):
    done: jax.Array  # [n_envs] episode ended at this step
    action: jax.Array  # [n_envs, n_agents]
    value: jax.Array  # [n_envs, n_agents]
    reward: jax.Array  # [n_envs] team reward
    log_prob: jax.Array  # [n_envs, n_agents]
    obs_grid: jax.Array  # [n_envs, n_agents, k, k, N_PLANES]
    obs_vec: jax.Array  # [n_envs, n_agents, 4]
    finished_return: jax.Array  # [n_envs] episodic return where done, else 0
    ep_metrics: dict  # M1.4 {name: [n_envs]} episode metrics, done-masked


# Episode metrics surfaced at done (M1.4): info key -> logged metric name.
EP_METRICS = {
    "survival_rate": "survival_rate",
    "completion": "completion",
    "ep_deaths_fire": "deaths_fire",
    "ep_deaths_collapse": "deaths_collapse",
    "mean_smoke_exposure": "mean_smoke_exposure",  # Phase-2 (M2.5 report)
}


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


class Runner(NamedTuple):
    """Carry of the training loop. `hyper` holds the PBT-mutable
    hyperparameters (lr, ent_coef) as traced float32 scalars so a population
    vmap can give every member its own values without recompiling."""

    train_state: TrainState
    hyper: dict
    env_states: object
    obs: dict
    ep_ret: jax.Array
    key: jax.Array


class TrainFns(NamedTuple):
    init: object  # jitted (key) -> Runner
    chunk: object  # jitted (Runner, n_updates static) -> (Runner, metrics)
    init_raw: object  # unjitted variants for population vmap (pbt.py)
    chunk_raw: object


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
            jnp.zeros((1, k, k, N_PLANES), jnp.float32),
            jnp.zeros((1, 4), jnp.float32),
        )
        # lr is applied manually in _update_minibatch (from Runner.hyper) so
        # PBT can mutate it per member at runtime; tx yields the Adam
        # direction only.
        tx = optax.chain(
            optax.clip_by_global_norm(tcfg.max_grad_norm),
            optax.scale_by_adam(eps=1e-5),
        )
        train_state = TrainState.create(apply_fn=network.apply, params=params, tx=tx)
        obs, env_states = jax.vmap(reset, in_axes=(0, None))(
            jax.random.split(k_reset, tcfg.n_envs), ecfg
        )
        hyper = {
            "lr": jnp.asarray(tcfg.lr, jnp.float32),
            "ent_coef": jnp.asarray(tcfg.ent_coef, jnp.float32),
        }
        ep_ret = jnp.zeros((tcfg.n_envs,), jnp.float32)
        return Runner(train_state, hyper, env_states, obs, ep_ret, key)

    def _env_step(runner, _):
        train_state, hyper, env_states, last_obs, ep_ret, key = runner
        key, k_sample, k_step = jax.random.split(key, 3)
        logits, value = network.apply(
            train_state.params, last_obs["grid"], last_obs["vec"]
        )
        pi = distrax.Categorical(logits=logits)
        action = pi.sample(seed=k_sample)
        log_prob = pi.log_prob(action)
        obs, env_states, reward, done, info = jax.vmap(
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
            ep_metrics={
                name: jnp.where(done, info[k].astype(jnp.float32), 0.0)
                for k, name in EP_METRICS.items()
            },
        )
        ep_ret = jnp.where(done, 0.0, ep_ret)
        return Runner(train_state, hyper, env_states, obs, ep_ret, key), trans

    def _loss_fn(params, mb, clip_eps, ent_coef):
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
        total = pg_loss + tcfg.vf_coef * v_loss - ent_coef * entropy
        return total, (pg_loss, v_loss, entropy)

    def _update_minibatch(carry, mb):
        train_state, hyper = carry
        grad_fn = jax.value_and_grad(_loss_fn, has_aux=True)
        (total, aux), grads = grad_fn(
            train_state.params, mb, tcfg.clip_eps, hyper["ent_coef"]
        )
        direction, opt_state = train_state.tx.update(
            grads, train_state.opt_state, train_state.params
        )
        updates = jax.tree_util.tree_map(lambda d: -hyper["lr"] * d, direction)
        train_state = train_state.replace(
            params=optax.apply_updates(train_state.params, updates),
            opt_state=opt_state,
            step=train_state.step + 1,
        )
        return (train_state, hyper), (total, *aux)

    def _update_epoch(update_state, _):
        train_state, hyper, batch, key = update_state
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
        (train_state, hyper), losses = jax.lax.scan(
            _update_minibatch, (train_state, hyper), minibatches
        )
        return (train_state, hyper, batch, key), losses

    def _update_once(runner, _):
        runner, traj = jax.lax.scan(_env_step, runner, None, tcfg.rollout_len)
        train_state, hyper, env_states, last_obs, ep_ret, key = runner
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
        (train_state, hyper, _, _), losses = jax.lax.scan(
            _update_epoch, (train_state, hyper, batch, k_update), None, tcfg.n_epochs
        )
        n_done = traj.done.sum()
        # M1.4: NaN-safe per-update means over finished episodes only.
        ep_means = {
            name: jnp.where(n_done > 0, vals.sum() / n_done, jnp.nan)
            for name, vals in traj.ep_metrics.items()
        }
        metrics = {
            "mean_return": jnp.where(
                n_done > 0, traj.finished_return.sum() / n_done, jnp.nan
            ),
            **ep_means,
            "n_episodes": n_done.astype(jnp.int32),
            "total_loss": losses[0].mean(),
            "pg_loss": losses[1].mean(),
            "v_loss": losses[2].mean(),
            "entropy": losses[3].mean(),
            "lr": hyper["lr"],
            "ent_coef": hyper["ent_coef"],
        }
        return Runner(train_state, hyper, env_states, last_obs, ep_ret, key), metrics

    def chunk_raw(runner, n_updates: int):
        return jax.lax.scan(_update_once, runner, None, n_updates)

    return TrainFns(
        init=jax.jit(init_runner),
        chunk=jax.jit(chunk_raw, static_argnames="n_updates"),
        init_raw=init_runner,
        chunk_raw=chunk_raw,
    )


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


def _save(mngr, runner: Runner, update: int):
    mngr.save(
        update,
        args=ocp.args.StandardSave(
            {
                "params": runner.train_state.params,
                "opt_state": runner.train_state.opt_state,
                "hyper": runner.hyper,
                "key": runner.key,
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
            template = {
                "params": runner.train_state.params,
                "opt_state": runner.train_state.opt_state,
                "hyper": runner.hyper,
                "key": runner.key,
                "update": 0,
            }
            restored = mngr.restore(start, args=ocp.args.StandardRestore(template))
            runner = runner._replace(
                train_state=runner.train_state.replace(
                    params=restored["params"], opt_state=restored["opt_state"]
                ),
                hyper=restored["hyper"],
                key=restored["key"],
            )
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

                def recent_mean(name):
                    vals = [
                        r[name]
                        for r in history[-20:]
                        if r[name] == r[name]  # drop NaN
                    ]
                    return sum(vals) / len(vals) if vals else float("nan")

                print(
                    f"[ippo] update {update}/{n_updates} "
                    f"return~{recent_mean('mean_return'):.2f} "
                    f"survival~{recent_mean('survival_rate'):.2f} "
                    f"completion~{recent_mean('completion'):.2f} "
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


def random_baseline(cfg: Config, *, n_episodes: int = 64, seed: int = 0) -> dict:
    """Uniform-random-policy episode metrics (the acceptance bar).

    M1.5: the Phase-1 acceptance compares completion AND survival_rate, so
    the baseline reports the full episode-metric row, not just return.
    """
    ecfg = cfg.env
    policy = make_random_policy(ecfg.n_agents)
    rewards, _, infos = jax.jit(
        lambda k: batch_rollout(k, ecfg, policy, ecfg.horizon, n_episodes)
    )(jax.random.PRNGKey(seed))
    final = {k: v[:, -1] for k, v in infos.items()}  # values at done
    return {
        "mean_return": float(rewards.sum(axis=1).mean()),
        "survival_rate": float(final["survival_rate"].mean()),
        "completion": float(final["completion"].mean()),
        "deaths_fire": float(
            final["ep_deaths_fire"].astype(jnp.float32).mean()
        ),
        "deaths_collapse": float(
            final["ep_deaths_collapse"].astype(jnp.float32).mean()
        ),
        "mean_smoke_exposure": float(final["mean_smoke_exposure"].mean()),
        "n_episodes": n_episodes,
    }


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
    p.add_argument("--death-penalty", type=float, default=None,
                   help="override theta.death_penalty (M1.5 acceptance)")
    p.add_argument("--baseline", action="store_true",
                   help="print the random-policy baseline metrics and exit")
    args = p.parse_args()
    cfg = load_config(args.config)
    if args.grid_size:
        cfg = dataclasses.replace(
            cfg, env=dataclasses.replace(cfg.env, grid_size=args.grid_size)
        )
    if args.death_penalty is not None:
        cfg = dataclasses.replace(
            cfg,
            env=dataclasses.replace(
                cfg.env,
                theta=dataclasses.replace(
                    cfg.env.theta, death_penalty=args.death_penalty
                ),
            ),
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
        print(json.dumps(random_baseline(cfg)))
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
