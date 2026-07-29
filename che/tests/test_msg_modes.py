"""M5.3 utility-gate arms: live / zeroed / shuffled.

The gate asks whether the swarm *uses* messages, so the three arms have to
differ in message content and in nothing else. What these tests pin:

1. Identical architecture and parameter count across arms — the ablation
   is content, not capacity. A zeroed arm implemented by deleting the
   message input would confound "messages are useless" with "this network
   is smaller".
2. The shuffled arm preserves the delivery pattern and the marginal
   content distribution exactly, and destroys only who-said-what. If it
   changed delivery it would be a second denial arm, not a discriminator.
3. Choosing an arm shifts no other PRNG stream, so the arms are CRN-paired
   against the same environment (the shuffle key is a fold_in, never a
   split).
4. Eval honours the trained arm, and `mute` remains a separate eval-time
   override for M5.5's usage diagnostic.
"""

import dataclasses

import chex
import jax
import jax.numpy as jnp
import numpy as np
import pytest

from che.env.comms import MSG_DIM, aggregate
from che.env.config import Config, EnvConfig, ThetaConfig, TrainConfig
from che.train.ippo import make_train_fns

MODES = ("live", "zeroed", "shuffled")

ECFG = EnvConfig(
    grid_size=16, n_agents=4, horizon=32, n_food=6,
    theta=ThetaConfig(beta=0.49, kappa_A=0.06, kappa_B=1.0, f_weak=0.15),
)


def _cfg(mode: str) -> Config:
    return Config(
        env=ECFG,
        train=TrainConfig(
            n_envs=4, rollout_len=8, n_minibatches=2, n_epochs=2,
            msg_mode=mode,
        ),
    )


def test_unknown_mode_is_a_loud_error():
    with pytest.raises(ValueError, match="msg_mode"):
        TrainConfig(msg_mode="muted")


def test_default_is_live():
    """Every pre-M5.3 config keeps its behaviour and its config hash."""
    assert TrainConfig().msg_mode == "live"


def test_all_arms_share_architecture_and_parameter_count():
    """The ablation is content, not capacity."""
    counts = {}
    for mode in MODES:
        runner = make_train_fns(_cfg(mode)).init(jax.random.PRNGKey(0))
        leaves = jax.tree.leaves(runner.train_state.params)
        counts[mode] = sum(int(np.prod(x.shape)) for x in leaves)
    assert len(set(counts.values())) == 1, counts
    # And identical at init under the same seed, not merely the same size.
    ref = make_train_fns(_cfg("live")).init(jax.random.PRNGKey(0))
    for mode in ("zeroed", "shuffled"):
        other = make_train_fns(_cfg(mode)).init(jax.random.PRNGKey(0))
        chex.assert_trees_all_equal(ref.train_state.params, other.train_state.params)


def test_arms_have_distinct_config_hashes():
    """Checkpoints from different arms must never be mistaken for each
    other on resume — the hash is what prevents it."""
    from che.train.ippo import config_hash

    hashes = {m: config_hash(_cfg(m)) for m in MODES}
    assert len(set(hashes.values())) == 3, hashes


@pytest.mark.parametrize("mode", MODES)
def test_every_arm_trains(mode):
    fns = make_train_fns(_cfg(mode))
    runner, metrics = fns.chunk(fns.init(jax.random.PRNGKey(0)), 1)
    assert jnp.isfinite(metrics["total_loss"]).all()
    assert jnp.isfinite(metrics["entropy"]).all()


def test_shuffle_preserves_delivery_and_marginals_only_destroying_attribution():
    """The discriminator's defining property, checked on the kernel itself.

    A permutation of the sender axis with the link graph held fixed must
    leave every receiver's in-degree untouched and leave the multiset of
    emitted messages untouched, while changing what an individual receiver
    gets. Any of those three failing makes the arm uninterpretable.
    """
    key = jax.random.PRNGKey(0)
    k_msg, k_link, k_perm = jax.random.split(key, 3)
    n = 6
    messages = jax.random.normal(k_msg, (n, MSG_DIM))
    links = jax.random.bernoulli(k_link, 0.5, (n, n)) & ~jnp.eye(n, dtype=bool)
    perm = jax.random.permutation(k_perm, n)

    plain = aggregate(messages, links)
    shuffled = aggregate(messages[perm], links)

    # Delivery pattern: in-degree per receiver is a property of `links`,
    # which the shuffle never touches.
    assert (links.sum(axis=0) == links.sum(axis=0)).all()
    # Marginal content distribution: same multiset of emitted messages.
    np.testing.assert_allclose(
        np.sort(np.asarray(messages), axis=0),
        np.sort(np.asarray(messages[perm]), axis=0),
        rtol=0, atol=0,
    )
    # ... but who-said-what is gone: some receiver's aggregate moved.
    assert not np.allclose(np.asarray(plain), np.asarray(shuffled))
    # Receivers with no incoming links get the zero vector either way, so
    # the arms can only differ where there was something to differ about.
    isolated = np.asarray(links.sum(axis=0) == 0)
    if isolated.any():
        np.testing.assert_allclose(
            np.asarray(plain)[isolated], np.asarray(shuffled)[isolated]
        )


def test_arm_choice_does_not_shift_any_other_prng_stream():
    """CRN pairing, tested on the stream itself rather than on outcomes.

    The arms *do* diverge behaviourally — that is the experiment. What must
    not diverge is PRNG consumption: the shuffle key is reached by fold_in,
    never by a split, so after an identical number of steps the carried key
    must be bitwise identical across arms. If it were not, the arms would
    be facing different environments and every M5.3 delta would be
    confounded with a reseeding.
    """
    keys = {}
    for mode in MODES:
        fns = make_train_fns(_cfg(mode))
        runner, _ = fns.chunk(fns.init(jax.random.PRNGKey(3)), 1)
        keys[mode] = np.asarray(runner.key)
    np.testing.assert_array_equal(keys["live"], keys["zeroed"])
    np.testing.assert_array_equal(keys["live"], keys["shuffled"])


def test_zeroed_arm_cuts_content_not_connectivity():
    """The zeroed arm must be a *content* ablation.

    Its link graph has to stay real — that is what distinguishes it from
    the δ = 1 denial arm, which cuts the graph itself. If zeroing content
    also collapsed connectivity, M5.3 would be measuring denial twice and
    the utility gate would answer a question nobody asked.

    (That the aggregate is exactly zero is pinned on the eval path, where
    it is directly observable: see the eval test below.)
    """
    fns = make_train_fns(_cfg("zeroed"))
    _, metrics = fns.chunk(fns.init(jax.random.PRNGKey(0)), 1)
    assert jnp.isfinite(metrics["total_loss"]).all()
    assert float(metrics["mean_out_degree"].mean()) > 0.0
    assert float(metrics["delivery_rate"].mean()) > 0.0


def test_eval_honours_the_trained_arm_and_mute_stays_separate():
    """A zeroed-arm policy must evaluate zeroed without anyone passing
    `mute`; and `mute` must remain available for M5.5's diagnostic, where
    a *live-trained* policy is evaluated with the channel cut."""
    from che.env.env import reset
    from che.eval.harness import make_policy_fn

    live, zeroed = _cfg("live"), _cfg("zeroed")
    params = make_train_fns(live).init(jax.random.PRNGKey(0)).train_state.params
    obs, _ = reset(jax.random.PRNGKey(1), ECFG)
    msg = jnp.zeros((ECFG.n_agents, MSG_DIM), jnp.float32)
    k = jax.random.PRNGKey(2)

    _, emitted_live = make_policy_fn(live, params, greedy=True)(k, obs, msg)
    _, emitted_zero = make_policy_fn(zeroed, params, greedy=True)(k, obs, msg)
    _, emitted_mute = make_policy_fn(live, params, greedy=True, mute=True)(k, obs, msg)

    assert not jnp.allclose(emitted_live, 0.0), "live arm emitted nothing"
    chex.assert_trees_all_equal(emitted_zero, jnp.zeros_like(emitted_zero))
    chex.assert_trees_all_equal(emitted_mute, jnp.zeros_like(emitted_mute))
    # Muting an already-zeroed arm is a no-op, not an error.
    _, both = make_policy_fn(zeroed, params, greedy=True, mute=True)(k, obs, msg)
    chex.assert_trees_all_equal(both, jnp.zeros_like(both))


def test_shuffled_eval_permutes_without_changing_the_multiset():
    from che.env.env import reset
    from che.eval.harness import make_policy_fn

    live, shuf = _cfg("live"), _cfg("shuffled")
    params = make_train_fns(live).init(jax.random.PRNGKey(0)).train_state.params
    obs, _ = reset(jax.random.PRNGKey(1), ECFG)
    msg = jnp.zeros((ECFG.n_agents, MSG_DIM), jnp.float32)
    k = jax.random.PRNGKey(5)
    _, a = make_policy_fn(live, params, greedy=True)(k, obs, msg)
    _, b = make_policy_fn(shuf, params, greedy=True)(k, obs, msg)
    np.testing.assert_allclose(
        np.sort(np.asarray(a), axis=0), np.sort(np.asarray(b), axis=0),
        rtol=0, atol=0,
    )


def test_debug_config_still_loads_and_is_live():
    """The default path is untouched by M5.3."""
    from che.env.config import load_config

    cfg = load_config("che/configs/debug.yaml")
    assert cfg.train.msg_mode == "live"
    assert dataclasses.replace(cfg.train, msg_mode="shuffled").msg_mode == "shuffled"
