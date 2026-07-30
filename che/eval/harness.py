"""M3.0 evaluation harness: load an orbax checkpoint (config-hash guarded),
run N vmap'd eval episodes with the policy as-trained (stochastic; greedy
optional), and emit per-episode metrics to npz + a summary JSON.

Episodes are fixed-length (done iff t == horizon, see env.step), so
per-episode values are the final-step entries of the info dict; the
coupling-co-active count (invariant #5) is a per-step counter and is summed
over the episode.

No training-code changes: the restore template and config hash come from
che.train.ippo (make_train_fns / config_hash), so the checkpoint tree layout
stays defined in exactly one place.
"""

import argparse
import dataclasses
import datetime
import json
from pathlib import Path

import distrax
import jax
import jax.numpy as jnp
import numpy as np
import orbax.checkpoint as ocp

from che.env.config import Config, load_config
from che.env.env import N_ACTIONS
from che.env.observation import plane_scales, quantize_grid
from che.train.ippo import (
    _MSG_SHUFFLE_STREAM,
    _ckpt_manager,
    config_hash,
    make_train_fns,
)
from che.train.networks import ActorCritic
from che.train.rollout import PolicyFn, batch_rollout

# npz key -> (info key, per-episode reduction over the time axis)
_FINAL = "final"  # value at the last step (episode-cumulative in info)
_SUM = "sum"  # summed over steps (per-step counter in info)
_MEAN = "mean"  # averaged over steps (per-step rate in info)
EVAL_METRICS = {
    "completion": ("completion", _FINAL),
    "survival_rate": ("survival_rate", _FINAL),
    "deaths_fire": ("ep_deaths_fire", _FINAL),
    "deaths_collapse": ("ep_deaths_collapse", _FINAL),
    "mean_smoke_exposure": ("mean_smoke_exposure", _FINAL),
    "coupling_co_active": ("coupling_co_active", _SUM),
    # M3.4-lock addendum: realized structural channels under trained
    # policies (drift check vs the random-policy calibration values, and
    # the non-ignition channels at High).
    "collapse_events": ("collapse_events", _SUM),
    "seeded_ignitions": ("seeded_ignitions", _SUM),
    "blocked_moves": ("blocked_moves", _SUM),
    "weak_occupancy": ("weak_occupancy", _MEAN),
    # M4.0 harness addendum (Phase-4 carry-overs): final burnt share and
    # the episode-mean masked crop share (0 until M4.1's obs v3 mask).
    "burnt_fraction": ("burnt_fraction", _FINAL),
    "masked_frac": ("masked_frac", _MEAN),
    # M4.4 addendum (a): danger-moment masking, carried as poolable
    # numerator/denominator sums rather than a ratio — the per-episode
    # conditional mean is masked_danger_sum / danger_agents, and pooling
    # across episodes weights each danger agent-step equally instead of
    # letting episodes with almost no fire dominate.
    "masked_danger_sum": ("masked_danger_sum", _SUM),
    "danger_agents": ("danger_agents", _SUM),
    "alive_agents": ("alive_agents", _SUM),
    # M5.0 comms channel (Def. 7), same poolable numerator/denominator
    # discipline: per-episode delivery rate = links_alive / links_in_range,
    # mean alive out-degree = links_alive / alive_agents. Kept as sums so
    # pooling across episodes weights each ordered pair (resp. agent-step)
    # equally rather than each episode.
    "links_alive": ("links_alive", _SUM),
    "links_in_range": ("links_in_range", _SUM),
}


def load_params(
    ckpt_dir: str | Path,
    cfg: Config,
    step: int | None = None,
    allow_hashes: tuple[str, ...] = (),
) -> tuple[dict, int]:
    """Restore policy params from an ippo.train checkpoint dir.

    Config-hash guarded: `ckpt_dir/config_hash.txt` must exist and match
    config_hash(cfg) — refuse to evaluate a policy under a config it was not
    trained with. Returns (params, restored_update_step).

    M3.0b forward-compat: `allow_hashes` names legacy hashes that are
    accepted despite a mismatch (config-schema changes move the hash of an
    unchanged physical config; e.g. M3.1 fields vs the M3.0 checkpoints).
    Explicit and per-hash only — the caller is responsible for recording
    the mapping in the eval provenance (see main()); never silent.
    """
    ckpt_dir = Path(ckpt_dir)
    hash_file = ckpt_dir / "config_hash.txt"
    if not hash_file.exists():
        raise ValueError(
            f"no config_hash.txt in {ckpt_dir} — not an ippo checkpoint dir"
        )
    stored = hash_file.read_text()
    if stored != config_hash(cfg) and stored not in allow_hashes:
        raise ValueError("checkpoint config hash mismatch — refusing to evaluate")
    mngr = _ckpt_manager(ckpt_dir)
    if step is None:
        step = mngr.latest_step()
    if step is None:
        raise ValueError(f"no checkpoint steps found in {ckpt_dir}")
    runner = make_train_fns(cfg).init(jax.random.PRNGKey(0))
    template = {
        "params": runner.train_state.params,
        "opt_state": runner.train_state.opt_state,
        "hyper": runner.hyper,
        "key": runner.key,
        "update": 0,
    }
    restored = mngr.restore(step, args=ocp.args.StandardRestore(template))
    return restored["params"], int(step)


def make_policy_fn(
    cfg: Config, params: dict, *, greedy: bool = False, mute: bool = False
) -> PolicyFn:
    """Policy for rollout_episode: stochastic as-trained, or argmax.

    M5.0: consumes the delivered aggregate and emits this step's message.
    `mute=True` hard-zeroes the *emitted* message, which makes every
    delivered aggregate the zero vector one step later — the message-zeroed
    arm of the M5.3 utility gate, at identical architecture and parameter
    count (the zeroing is at the aggregation point, not a different net).

    M5.1f: when the checkpoint was trained with uint8 obs storage, eval
    quantizes too. Evaluating a uint8-trained policy on unquantized crops
    would be a train/eval input mismatch — small, but exactly the kind of
    unforced discrepancy that later shows up as an unexplained gap. The
    config hash keeps the two modes from being mixed by accident.

    M5.3: `cfg.train.msg_mode` is honoured here too, so an arm is evaluated
    under the regime it was trained under. `mute` stays a separate,
    eval-time override — it is what M5.5's message-usage diagnostic needs
    (zero the channel on a policy that was *trained* with it live), which
    is a different question from M5.3's trained-arm comparison. Setting
    `mute` on an already-zeroed arm is a no-op, as it should be.
    """
    ecfg, tcfg = cfg.env, cfg.train
    net = ActorCritic(N_ACTIONS, obs_scale=plane_scales(ecfg))

    def policy(
        key: jax.Array, obs: dict[str, jax.Array], msg: jax.Array
    ) -> tuple[jax.Array, jax.Array]:
        grid = quantize_grid(obs["grid"], ecfg) if tcfg.uint8_obs else obs["grid"]
        logits, _, emitted = net.apply(params, grid, obs["vec"], msg)
        if mute or tcfg.msg_mode == "zeroed":  # static — its own jitted policy
            emitted = jnp.zeros_like(emitted)
        elif tcfg.msg_mode == "shuffled":
            # Sender-axis permutation, as in training. rollout_episode is
            # single-env here, so this permutes the agent axis directly.
            # fold_in, not the raw key: `key` already seeds the action
            # sample below and a key is never reused.
            emitted = emitted[
                jax.random.permutation(
                    jax.random.fold_in(key, _MSG_SHUFFLE_STREAM),
                    emitted.shape[0],
                )
            ]
        if greedy:  # static Python flag — two distinct jitted policies
            return jnp.argmax(logits, axis=-1).astype(jnp.int32), emitted
        return (
            distrax.Categorical(logits=logits).sample(seed=key).astype(jnp.int32),
            emitted,
        )

    return policy


def evaluate(
    cfg: Config,
    params: dict,
    *,
    n_episodes: int = 512,
    seed: int = 0,
    greedy: bool = False,
    mute: bool = False,
) -> dict[str, np.ndarray]:
    """Run n_episodes vmap'd fixed-length episodes; return per-episode arrays.

    Every array has shape [n_episodes]; `episode_return` is the summed team
    reward, the rest follow EVAL_METRICS.
    """
    policy = make_policy_fn(cfg, params, greedy=greedy, mute=mute)
    ecfg = cfg.env
    rewards, _, infos = jax.jit(
        lambda k: batch_rollout(k, ecfg, policy, ecfg.horizon, n_episodes)
    )(jax.random.PRNGKey(seed))
    out = {"episode_return": np.asarray(rewards.sum(axis=1), np.float32)}
    for name, (info_key, red) in EVAL_METRICS.items():
        vals = infos[info_key]
        if red == _FINAL:
            per_ep = vals[:, -1]
        elif red == _MEAN:
            per_ep = vals.mean(axis=1)
        else:
            per_ep = vals.sum(axis=1)
        out[name] = np.asarray(per_ep.astype(jnp.float32))
    return out


def summarize(per_episode: dict[str, np.ndarray]) -> dict:
    """Mean, std (ddof=1), and quartiles per metric."""
    summary = {}
    for name, vals in per_episode.items():
        q25, q50, q75 = np.percentile(vals, [25, 50, 75])
        summary[name] = {
            "mean": float(vals.mean()),
            "std": float(vals.std(ddof=1)),
            "q25": float(q25),
            "median": float(q50),
            "q75": float(q75),
            "min": float(vals.min()),
            "max": float(vals.max()),
        }
    return summary


def main(argv: list[str] | None = None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", required=True)
    p.add_argument("--ckpt-dir", required=True)
    p.add_argument("--step", type=int, help="checkpoint step (default: latest)")
    p.add_argument("--n-episodes", type=int, default=512)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument(
        "--greedy",
        action="store_true",
        help="argmax policy instead of as-trained sampling",
    )
    p.add_argument(
        "--death-penalty",
        type=float,
        default=None,
        help="theta override — must match the training run (hash guard)",
    )
    p.add_argument(
        "--kappa-A",
        type=float,
        default=None,
        dest="kappa_A",
        help="theta override — must match the training run "
        "(M3.5 kappa_A ablation arm; hash guard)",
    )
    p.add_argument(
        "--kappa-B",
        type=float,
        default=None,
        dest="kappa_B",
        help="theta override — must match the training run "
        "(M4.3 probe policies / M4.4 kappa_B arm; hash guard)",
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
        help="theta override — must match the training run "
        "(M5.3b sensitivity cell / M5.4 sweep; hash guard)",
    )
    p.add_argument(
        "--obs-version",
        type=int,
        default=None,
        choices=(1, 2, 3),
        help="override cfg obs_version — archival eval of obs-v1/v2 "
        "checkpoints only (D5/M4.1); never compare across versions",
    )
    p.add_argument(
        "--allow-hash",
        action="append",
        default=[],
        metavar="HASH",
        help="accept this named legacy checkpoint hash despite a "
        "config-hash mismatch (repeatable); the old->current "
        "mapping is recorded in the summary JSON",
    )
    p.add_argument(
        "--msg-mode",
        choices=("live", "zeroed", "shuffled"),
        default=None,
        dest="msg_mode",
        help="M5.3 arm — must match the training run (hash guard)",
    )
    p.add_argument(
        "--mute",
        action="store_true",
        help="zero the emitted message at EVAL time on a policy trained "
        "with it live (M5.5 message-usage diagnostic). Distinct from "
        "--msg-mode zeroed, which is a trained arm and changes the hash",
    )
    p.add_argument("--out-npz", required=True, help="per-episode arrays output")
    p.add_argument("--out-json", help="summary JSON output (default: npz stem + .json)")
    args = p.parse_args(argv)

    cfg = load_config(args.config)
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
    if args.obs_version is not None:
        cfg = dataclasses.replace(
            cfg, env=dataclasses.replace(cfg.env, obs_version=args.obs_version)
        )
    if args.msg_mode is not None:
        cfg = dataclasses.replace(
            cfg, train=dataclasses.replace(cfg.train, msg_mode=args.msg_mode)
        )
    params, step = load_params(
        args.ckpt_dir, cfg, step=args.step, allow_hashes=tuple(args.allow_hash)
    )
    stored_hash = (Path(args.ckpt_dir) / "config_hash.txt").read_text()
    current_hash = config_hash(cfg)
    hash_compat = None
    if stored_hash != current_hash:  # only reachable via --allow-hash
        hash_compat = {
            "ckpt_hash": stored_hash,
            "current_hash": current_hash,
            "allow_hash_flag": list(args.allow_hash),
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        }
        print(
            f"WARNING: legacy checkpoint hash {stored_hash} accepted via "
            f"--allow-hash (current config hash {current_hash}); "
            "mapping recorded in summary JSON"
        )
    per_episode = evaluate(
        cfg,
        params,
        n_episodes=args.n_episodes,
        seed=args.seed,
        greedy=args.greedy,
        mute=args.mute,
    )
    out_npz = Path(args.out_npz)
    out_npz.parent.mkdir(parents=True, exist_ok=True)
    np.savez(out_npz, **per_episode)
    summary = {
        "config": args.config,
        "config_hash": config_hash(cfg),
        "ckpt_dir": args.ckpt_dir,
        "ckpt_step": step,
        "n_episodes": args.n_episodes,
        "seed": args.seed,
        "greedy": args.greedy,
        "obs_version": cfg.env.obs_version,
        # M5.3/M5.5: which arm this is, and whether the channel was cut at
        # eval time. Two different questions, so both are recorded — a
        # summary that showed only one would be ambiguous.
        "msg_mode": cfg.train.msg_mode,
        "eval_muted": args.mute,
        "metrics": summarize(per_episode),
    }
    if hash_compat is not None:
        summary["hash_compat"] = hash_compat
    out_json = Path(args.out_json) if args.out_json else out_npz.with_suffix(".json")
    out_json.write_text(json.dumps(summary, indent=1) + "\n")
    print(json.dumps(summary["metrics"], indent=1))


if __name__ == "__main__":
    main()
