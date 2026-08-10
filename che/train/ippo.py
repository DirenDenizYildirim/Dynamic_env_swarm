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

from che.env.comms import MSG_DIM, aggregate
from che.env.config import MAX_MIXTURE_COMPONENTS, Config, load_config
from che.env.env import N_ACTIONS, reset
from che.env.observation import n_planes, plane_scales, quantize_grid
from che.train.networks import ActorCritic
from che.train.rollout import batch_rollout, make_random_policy, step_autoreset


class Transition(NamedTuple):
    done: jax.Array  # [n_envs] episode ended at this step
    action: jax.Array  # [n_envs, n_agents]
    value: jax.Array  # [n_envs, n_agents]
    reward: jax.Array  # [n_envs] team reward
    log_prob: jax.Array  # [n_envs, n_agents]
    obs_grid: jax.Array  # [n_envs, n_agents, k, k, n_planes(cfg.env)]
    obs_vec: jax.Array  # [n_envs, n_agents, 4]
    # M5.0: the delivered message aggregate is part of the policy *input*,
    # so it must be stored and replayed by the loss exactly like obs — else
    # the surrogate would recompute log-probs against different inputs than
    # the ones the action was sampled from. Storing it (rather than
    # recomputing messages inside the loss) is also what makes the channel
    # non-differentiable, per the Q3 ruling; see networks.py.
    obs_msg: jax.Array  # [n_envs, n_agents, MSG_DIM]
    finished_return: jax.Array  # [n_envs] episodic return where done, else 0
    ep_metrics: dict  # M1.4 {name: [n_envs]} episode metrics, done-masked
    # M5.0 comms diagnostics, pooled as numerator/denominator over the whole
    # update (never done-masked: these are per-step channel properties, not
    # episode outcomes).
    links_alive: jax.Array  # [n_envs]
    links_in_range: jax.Array  # [n_envs]
    alive_agents: jax.Array  # [n_envs] out-degree denominator
    # E1 addendum (human-instructed 2026-08-04): the coupling counters,
    # pooled over the update exactly like the comms pair above and for the
    # same reason -- they are PER-STEP counts, not episode-end values, so
    # done-masking them would record only whatever the final step happened
    # to hold. {name: [n_envs]}.
    step_metrics: dict


# M5.3: dedicated stream id for the shuffled-arm permutation, following the
# env's convention (env.py _OBS_STREAM 47 / _COMMS_STREAM 53). Reached by
# fold_in, never by a split, so selecting an arm shifts no other stream.
_MSG_SHUFFLE_STREAM = 71

# Episode metrics surfaced at done (M1.4): info key -> logged metric name.
EP_METRICS = {
    "survival_rate": "survival_rate",
    "completion": "completion",
    "ep_deaths_fire": "deaths_fire",
    "ep_deaths_collapse": "deaths_collapse",
    "mean_smoke_exposure": "mean_smoke_exposure",  # Phase-2 (M2.5 report)
    # M6.0c (spike acceptance 2d): which mixture component each finished
    # episode was drawn from. Done-masked and averaged over finished
    # episodes like every other entry here, so for the spike's TWO-component
    # mixture (labels 0/1) the logged mean IS the realized weight of
    # component 1 — the audit the acceptance asks for.
    # LIMITATION, stated rather than discovered later: a mean over component
    # INDICES only reads as a mixture ratio for two components. Phase 6's
    # four-component design needs per-component counts, which is a logging
    # change (one channel per component, or a one-hot sum), not a mechanism
    # change. Deliberately out of the spike's 2-component scope fence.
    "mixture_component": "mixture_component",
    # M6.1: per-component realized weights. Each averages, done-masked over
    # finished episodes, to the fraction of episodes drawn from that
    # component — the audit the registered design needs at up to 8
    # components, where the index mean above stops meaning anything.
    **{f"mixture_count_{i}": f"mixture_w{i}" for i in range(MAX_MIXTURE_COMPONENTS)},
}

# E1 addendum (human-instructed 2026-08-04): PER-STEP coupling counters,
# pooled over the update -- info key -> logged metric name.
#
# WHY THESE ARE NOT IN EP_METRICS. Everything above is an episode-END value,
# recorded by masking on `done`. These are per-step COUNTS: the number of
# collapse-seeded ignitions near an agent on THIS step, etc. Done-masking a
# count records whatever the last step held, which is not the episode total
# and not a rate. They are pooled over the whole update instead, exactly like
# the M5.0 comms pair.
#
# WHY THEY ARE LOGGED AT ALL. Invariant #5 required the co-active counter to
# be logged "from day one" so that retrofitting it into jitted rollouts would
# never be necessary. The env emitted it and the eval harness consumed it, but
# the TRAINING logger never picked it up -- so the within-training trajectory
# of compound hostility was unmeasurable from any committed artifact
# (E1.2 section 7: 0 of 92 training logs carried it). This closes that gap at
# the layer where it was actually open.
#
# UNITS, stated because two conventions for one name is how this project gets
# hurt. These log the MEAN PER ENV-STEP. The eval npz reports the same
# channels SUMMED PER EPISODE. Multiplying by the horizon converts, and is
# exact only for episodes that run to the horizon -- treat it as an
# approximation, and prefer comparing training curves to each other.
STEP_METRICS = {
    "coupling_co_active": "co_active_per_step",
    "seeded_ignitions": "seeded_ignitions_per_step",
    "collapse_events": "collapse_events_per_step",
    "danger_agents": "danger_agents_per_step",
    "masked_danger_sum": "masked_danger_sum_per_step",
    "blocked_moves": "blocked_moves_per_step",
    # Render-gate diagnostic (registrar 2026-08-10): positional drift, shipped
    # before the grid so 240 runs measure it for free -- the same
    # cheap-now-impossible-later window invariant #5 was written to protect,
    # and the same layer (the training logger) where the co-active counter was
    # found half-satisfied. Read the pair as rates against alive_agents:
    # center_dist_sum_per_step / alive_agents_per_step is the mean Chebyshev
    # distance from the arena centre per surviving agent, and
    # boundary_agents_per_step / alive_agents_per_step is the boundary-contact
    # fraction -- the direct wall-pile-up statistic.
    "center_dist_sum": "center_dist_sum_per_step",
    "boundary_agents": "boundary_agents_per_step",
    # THE DENOMINATOR, and why it is here. The two channels above are sums over
    # ALIVE agents, so undenominated they fall as agents die and confound
    # positional drift with mortality -- at High, where survival moves 8.8
    # points between arms, that confound is larger than the effect. This is
    # already in EVAL_METRICS and already in the Transition below; the training
    # log is catching up to the eval path. It also retroactively makes
    # danger_agents_per_step above readable as a rate rather than a count.
    "alive_agents": "alive_agents_per_step",
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
    vmap can give every member its own values without recompiling.

    M5.0 adds `messages` [n_envs, n_agents, MSG_DIM]: the messages emitted
    last step and delivered this step (comms.py). It is carry state, not
    checkpoint state — resume starts it at zeros along with the env states,
    which costs one step of in-flight traffic and keeps the checkpoint tree
    unchanged."""

    train_state: TrainState
    hyper: dict
    env_states: object
    obs: dict
    ep_ret: jax.Array
    key: jax.Array
    messages: jax.Array


class TrainFns(NamedTuple):
    init: object  # jitted (key) -> Runner
    chunk: object  # jitted (Runner, n_updates static) -> (Runner, metrics)
    init_raw: object  # unjitted variants for population vmap (pbt.py)
    chunk_raw: object


@functools.lru_cache(maxsize=8)
def make_train_fns(cfg: Config) -> TrainFns:
    """Build (and cache per-config) the jitted init and K-update-chunk fns."""
    ecfg, tcfg = cfg.env, cfg.train
    # M5.1f: quantize once per step, then act AND update on the same stored
    # values. Acting on float32 while replaying uint8 would make the PPO
    # ratio differ from 1 in the first epoch — a silent bias, not a rounding
    # detail — so the collector never sees the float crop again.
    scales = plane_scales(ecfg)
    network = ActorCritic(N_ACTIONS, obs_scale=scales)
    obs_dtype = jnp.uint8 if tcfg.uint8_obs else jnp.float32

    def _store_grid(grid):
        return quantize_grid(grid, ecfg) if tcfg.uint8_obs else grid

    def init_runner(key: jax.Array):
        key, k_net, k_reset = jax.random.split(key, 3)
        k = ecfg.obs_window
        params = network.init(
            k_net,
            jnp.zeros((1, k, k, n_planes(ecfg)), obs_dtype),
            jnp.zeros((1, 4), jnp.float32),
            jnp.zeros((1, MSG_DIM), jnp.float32),
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
        messages = jnp.zeros((tcfg.n_envs, ecfg.n_agents, MSG_DIM), jnp.float32)
        return Runner(train_state, hyper, env_states, obs, ep_ret, key, messages)

    def _delivered(messages, obs, key):
        """Masked-mean aggregate of last step's messages over this step's
        realized links (M5.0), under the M5.3 arm in `tcfg.msg_mode`.

        The arms are static Python branches on a frozen config field, so
        each compiles to its own program with no traced branching — and
        `key` is a fold_in, not a split, so choosing an arm cannot shift
        any other PRNG stream. Live and zeroed therefore see bitwise the
        same environment as shuffled given the same seed.
        """
        if tcfg.msg_mode == "shuffled":
            # Permute the SENDER axis, independently per env. links is
            # untouched, so every receiver's in-degree and the multiset of
            # emitted messages are exactly preserved; what is destroyed is
            # the correspondence between a message and who sent it.
            n_env, n_ag = messages.shape[0], messages.shape[1]
            perms = jax.vmap(lambda k: jax.random.permutation(k, n_ag))(
                jax.random.split(key, n_env)
            )
            messages = jnp.take_along_axis(messages, perms[:, :, None], axis=1)
        agg = jax.vmap(aggregate)(messages, obs["links"])
        if tcfg.msg_mode == "zeroed":
            # Zero at the aggregation point, not by deleting the input: the
            # network keeps its message Dense layer and its parameter count,
            # so the arm differs from live in content alone.
            agg = jnp.zeros_like(agg)
        return agg

    def _env_step(runner, _):
        train_state, hyper, env_states, last_obs, ep_ret, key, messages = runner
        key, k_sample, k_step = jax.random.split(key, 3)
        delivered = _delivered(
            messages, last_obs, jax.random.fold_in(k_step, _MSG_SHUFFLE_STREAM)
        )
        obs_grid = _store_grid(last_obs["grid"])
        logits, value, emitted = network.apply(
            train_state.params, obs_grid, last_obs["vec"], delivered
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
            obs_grid=obs_grid,
            obs_vec=last_obs["vec"],
            obs_msg=delivered,
            finished_return=jnp.where(done, ep_ret, 0.0),
            ep_metrics={
                name: jnp.where(done, info[k].astype(jnp.float32), 0.0)
                for k, name in EP_METRICS.items()
            },
            links_alive=info["links_alive"],
            links_in_range=info["links_in_range"],
            alive_agents=info["alive_agents"],
            # Never done-masked -- see STEP_METRICS.
            step_metrics={
                name: info[k].astype(jnp.float32)
                for k, name in STEP_METRICS.items()
            },
        )
        ep_ret = jnp.where(done, 0.0, ep_ret)
        # Messages emitted this step are delivered next step. Nothing crosses
        # an episode boundary (autoreset), and stop_gradient states in code
        # what the batch-storage already implies: the channel is not a
        # differentiable path (Q3 ruling; networks.py docstring).
        messages = jax.lax.stop_gradient(
            jnp.where(done[:, None, None], 0.0, emitted)
        )
        return (
            Runner(train_state, hyper, env_states, obs, ep_ret, key, messages),
            trans,
        )

    # M5.1g: remat only the differentiated forward. The collector's forward
    # is not differentiated, so it retains nothing worth recomputing.
    _apply = jax.checkpoint(network.apply) if tcfg.remat else network.apply

    def _loss_fn(params, mb, clip_eps, ent_coef):
        # The emitted message is discarded here: no term of the loss depends
        # on it, which is exactly why the message head never receives a
        # gradient (Q3 ruling — networks.py documents the consequence).
        logits, value, _ = _apply(
            params, mb["obs_grid"], mb["obs_vec"], mb["obs_msg"]
        )
        pi = distrax.Categorical(logits=logits)
        log_prob = pi.log_prob(mb["action"])
        ratio = jnp.exp(log_prob - mb["log_prob"])
        adv = mb["adv"]
        adv = (adv - adv.mean()) / (adv.std() + 1e-8)
        pg_loss = -jnp.minimum(
            ratio * adv,
            jnp.clip(ratio, 1.0 - clip_eps, 1.0 + clip_eps) * adv,
        ).mean()
        v_clipped = mb["value"] + jnp.clip(value - mb["value"], -clip_eps, clip_eps)
        v_loss = (
            0.5
            * jnp.maximum(
                (value - mb["target"]) ** 2, (v_clipped - mb["target"]) ** 2
            ).mean()
        )
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
        train_state, hyper, env_states, last_obs, ep_ret, key, messages = runner
        _, last_value, _ = network.apply(
            train_state.params,
            _store_grid(last_obs["grid"]),
            last_obs["vec"],
            # Bootstrap value: same arm as the rollout saw, or the critic
            # would be evaluated on an input distribution the policy never
            # acted under. fold_in on the carried key keeps it deterministic
            # without consuming the stream.
            _delivered(
                messages, last_obs, jax.random.fold_in(key, _MSG_SHUFFLE_STREAM)
            ),
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
            "obs_msg": flat(traj.obs_msg),
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
            # M5.0: channel diagnostics pooled over every step of the update
            # (ratio of sums, not mean of ratios). delivery_rate ~ 1 - delta
            # once geometry is divided out; mean_out_degree is the M5.4 band
            # observable under the training policy. NaN when nobody was ever
            # in range, which is a real "no channel", not a zero.
            "delivery_rate": jnp.where(
                traj.links_in_range.sum() > 0,
                traj.links_alive.sum() / traj.links_in_range.sum(),
                jnp.nan,
            ),
            "mean_out_degree": traj.links_alive.sum()
            / jnp.maximum(traj.alive_agents.sum(), 1.0),
            # E1 addendum: coupling counters as a mean per env-step, pooled
            # over every step of the update. Not done-masked and never NaN --
            # a step with no co-active event is a real zero, unlike an update
            # with no finished episode, which is a real absence.
            **{
                name: vals.mean()
                for name, vals in traj.step_metrics.items()
            },
        }
        return (
            Runner(train_state, hyper, env_states, last_obs, ep_ret, key, messages),
            metrics,
        )

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
                raise ValueError("checkpoint config hash mismatch — refusing to resume")
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
        while update < n_updates and not (handle_sigterm and _SIGTERM["received"]):
            k = min(cfg.train.ckpt_interval, n_updates - update)
            t0 = time.perf_counter()
            runner, metrics = fns.chunk(runner, k)
            jax.block_until_ready(metrics["total_loss"])
            dt = time.perf_counter() - t0
            for i in range(k):
                row = {name: float(vals[i]) for name, vals in metrics.items()}
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
        "deaths_fire": float(final["ep_deaths_fire"].astype(jnp.float32).mean()),
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
    p.add_argument(
        "--death-penalty",
        type=float,
        default=None,
        help="override theta.death_penalty (M1.5 acceptance)",
    )
    p.add_argument(
        "--kappa-A",
        type=float,
        default=None,
        dest="kappa_A",
        help="override theta.kappa_A (M3.5 ablation arm)",
    )
    p.add_argument(
        "--kappa-B",
        type=float,
        default=None,
        dest="kappa_B",
        help="override theta.kappa_B (M4.3 probe policies / M4.4 arm)",
    )
    p.add_argument(
        "--delta",
        type=float,
        default=None,
        help="override theta.delta, the comms-denial level (Def. 7). "
        "M5.5 grid arm; changes the config hash, so every consumer of a "
        "checkpoint must pass the same value",
    )
    p.add_argument(
        "--r-comm",
        type=float,
        default=None,
        dest="r_comm",
        help="override theta.r_comm (M5.3b sensitivity cell / M5.4 sweep); "
        "changes the config hash, so eval must pass the same value",
    )
    p.add_argument(
        "--msg-mode",
        choices=("live", "zeroed", "shuffled"),
        default=None,
        dest="msg_mode",
        help="M5.3 utility-gate arm (default: the config's)",
    )
    p.add_argument(
        "--baseline",
        action="store_true",
        help="print the random-policy baseline metrics and exit",
    )
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
    if args.kappa_A is not None:
        cfg = dataclasses.replace(
            cfg,
            env=dataclasses.replace(
                cfg.env,
                theta=dataclasses.replace(cfg.env.theta, kappa_A=args.kappa_A),
            ),
        )
    if args.kappa_B is not None:
        cfg = dataclasses.replace(
            cfg,
            env=dataclasses.replace(
                cfg.env,
                theta=dataclasses.replace(cfg.env.theta, kappa_B=args.kappa_B),
            ),
        )
    if args.delta is not None:
        cfg = dataclasses.replace(
            cfg,
            env=dataclasses.replace(
                cfg.env,
                theta=dataclasses.replace(cfg.env.theta, delta=args.delta),
            ),
        )
    if args.r_comm is not None:
        cfg = dataclasses.replace(
            cfg,
            env=dataclasses.replace(
                cfg.env,
                theta=dataclasses.replace(cfg.env.theta, r_comm=args.r_comm),
            ),
        )
    train_overrides = {
        k: v
        for k, v in (
            ("n_envs", args.n_envs),
            ("rollout_len", args.rollout_len),
            ("msg_mode", args.msg_mode),
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
