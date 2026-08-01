"""M5.0 comms-axis tests: the link kernel, the message path, and the
delta-nesting invariant (CLAUDE.md #3).

The five the Phase-5 prompt names, plus the kernel properties they rest on:

1. delta cannot perturb any env kernel stream — state trajectories are
   bitwise-identical across delta under matched keys (at *fixed* action
   sequences: the whole point of comms is that it changes actions, so the
   invariant is about the kernels, not the policy).
2. delta = 1 => every delivered aggregate is the zero vector, bitwise.
3. A message-zeroed network reproduces delta = 1 outcomes given matched keys.
4. Aggregation is permutation-invariant in the senders.
5. Dead agents neither send nor deliver.
"""

import dataclasses

import chex
import jax
import jax.numpy as jnp
import numpy as np
import pytest

from che.env.comms import MSG_DIM, aggregate, in_range_mask, sample_links
from che.env.config import EnvConfig, ThetaConfig
from che.env.env import N_ACTIONS, reset, step
from che.env.types import EnvState
from che.train.networks import ActorCritic
from che.train.rollout import rollout_episode

CFG = EnvConfig(
    grid_size=16,
    n_agents=4,
    horizon=24,
    n_food=6,
    theta=ThetaConfig(
        beta=0.49, kappa_A=0.06, kappa_B=1.0, f_weak=0.15,
        lambda_0=5e-5, lambda_load=4e-4, r_comm=8.0,
    ),
)


def _with_delta(cfg: EnvConfig, delta: float) -> EnvConfig:
    return dataclasses.replace(
        cfg, theta=dataclasses.replace(cfg.theta, delta=delta)
    )


def _fixed_action_rollout(cfg: EnvConfig, key, n_steps: int = 12):
    """Roll the env forward on a *pre-drawn* action sequence and return the
    full state trajectory. Actions are fixed across configs so any state
    difference is the env's, not the policy's."""
    k_reset, k_act, k_steps = jax.random.split(key, 3)
    actions = jax.random.randint(
        k_act, (n_steps, cfg.n_agents), 0, N_ACTIONS, dtype=jnp.int32
    )
    _, state = reset(k_reset, cfg)
    keys = jax.random.split(k_steps, n_steps)

    def body(s, xs):
        k, a = xs
        _, s_new, r, _, info = step(k, s, a, cfg)
        return s_new, (s_new, r, info)

    _, (states, rewards, infos) = jax.lax.scan(body, state, (keys, actions))
    return states, rewards, infos


# --------------------------------------------------------------- kernel


def test_delta_zero_is_the_deterministic_range_graph():
    """delta = 0 keeps every in-range ordered pair — the nested model."""
    pos = jnp.array([[0, 0], [3, 3], [15, 15], [2, 9]], dtype=jnp.int32)
    alive = jnp.ones((4,), dtype=jnp.bool_)
    rng = in_range_mask(pos, alive, 8.0)
    links = sample_links(jax.random.PRNGKey(0), rng, 0.0)
    chex.assert_trees_all_equal(links, rng)


def test_delta_one_is_the_empty_graph():
    pos = jnp.zeros((4, 2), dtype=jnp.int32)  # everyone co-located, all in range
    alive = jnp.ones((4,), dtype=jnp.bool_)
    rng = in_range_mask(pos, alive, 8.0)
    assert int(rng.sum()) == 12  # 4*3 ordered pairs
    links = sample_links(jax.random.PRNGKey(0), rng, 1.0)
    assert not bool(links.any())


def test_range_is_chebyshev_and_hard():
    """d = max(|dr|, |dc|) <= R, a hard cutoff — the Q6-ruled kernel."""
    pos = jnp.array([[0, 0], [3, 3], [4, 0], [0, 5]], dtype=jnp.int32)
    alive = jnp.ones((4,), dtype=jnp.bool_)
    rng = np.asarray(in_range_mask(pos, alive, 4.0))
    assert rng[0, 1] and rng[0, 2]  # d = 3, 4  -> in range
    assert not rng[0, 3]  # d = 5 -> out
    assert not rng.diagonal().any()  # never self


def test_dead_agents_neither_send_nor_deliver():
    pos = jnp.zeros((3, 2), dtype=jnp.int32)  # all co-located
    alive = jnp.array([True, False, True])
    rng = np.asarray(in_range_mask(pos, alive, 8.0))
    assert not rng[1].any()  # agent 1 sends nothing
    assert not rng[:, 1].any()  # and receives nothing
    assert rng[0, 2] and rng[2, 0]  # the living pair still links


def test_link_draws_are_unconditional_in_delta():
    """Same key, different delta: the *uniforms* must be the same draw, so
    the delta = 0 graph contains every link the delta = 0.5 graph has
    (thinning, not a different random stream). Invariant #3."""
    key = jax.random.PRNGKey(3)
    pos = jax.random.randint(jax.random.PRNGKey(4), (8, 2), 0, 16, dtype=jnp.int32)
    alive = jnp.ones((8,), dtype=jnp.bool_)
    rng = in_range_mask(pos, alive, 8.0)
    full = sample_links(key, rng, 0.0)
    thinned = sample_links(key, rng, 0.5)
    denied = sample_links(key, rng, 1.0)
    assert bool((full | thinned == full).all())  # thinned subset of full
    assert not bool(denied.any())
    assert 0 < int(thinned.sum()) < int(full.sum())  # the knob actually moved


def test_directed_links_can_be_asymmetric():
    """One uniform per *ordered* pair (Q6): 0 < delta < 1 permits i->j
    without j->i. Physically legitimate — fading is directional."""
    key = jax.random.PRNGKey(7)
    pos = jnp.zeros((12, 2), dtype=jnp.int32)
    alive = jnp.ones((12,), dtype=jnp.bool_)
    links = np.asarray(sample_links(key, in_range_mask(pos, alive, 8.0), 0.5))
    assert (links != links.T).any()


# ------------------------------------------------------- aggregation


def test_aggregate_is_masked_mean_and_zero_when_isolated():
    messages = jnp.array(
        [[1.0] * MSG_DIM, [3.0] * MSG_DIM, [5.0] * MSG_DIM], jnp.float32
    )
    links = jnp.array(  # 0->2 and 1->2 deliver; nobody delivers to 0 or 1
        [[False, False, True], [False, False, True], [False, False, False]]
    )
    agg = aggregate(messages, links)
    np.testing.assert_allclose(np.asarray(agg[2]), np.full(MSG_DIM, 2.0))
    assert not np.asarray(agg[0]).any() and not np.asarray(agg[1]).any()


def test_aggregate_is_permutation_invariant_in_senders():
    key = jax.random.PRNGKey(11)
    k_m, k_l, k_p = jax.random.split(key, 3)
    n = 6
    messages = jax.random.normal(k_m, (n, MSG_DIM))
    links = jax.random.bernoulli(k_l, 0.5, (n, n)) & ~jnp.eye(n, dtype=jnp.bool_)
    perm = jax.random.permutation(k_p, n)
    base = aggregate(messages, links)
    # Permute sender identity: rows of `messages` and rows of `links`.
    permuted = aggregate(messages[perm], links[perm])
    chex.assert_trees_all_close(base, permuted, atol=1e-6)


def test_sender_message_is_never_self_delivered():
    """A lone agent, or an agent whose only in-range peer is itself, gets
    the zero vector — the diagonal is excluded from the graph, not zeroed
    after the fact."""
    messages = jnp.ones((1, MSG_DIM), jnp.float32)
    links = in_range_mask(
        jnp.zeros((1, 2), jnp.int32), jnp.ones((1,), jnp.bool_), 8.0
    )
    assert not bool(links.any())
    assert not np.asarray(aggregate(messages, links)).any()


# ----------------------------------------------------------- nesting


@pytest.mark.parametrize("delta", [0.0, 0.5, 1.0])
def test_delta_does_not_perturb_any_env_kernel_stream(delta):
    """Invariant #3 for the comms axis: at fixed actions and matched keys,
    every state component is bitwise-identical across delta. T_K reads x'
    and nothing reads k back, so the hazard/smoke/structure/agent streams
    cannot see the comms draw."""
    key = jax.random.PRNGKey(5)
    ref, _, _ = _fixed_action_rollout(CFG, key)  # CFG has delta = 0.0
    got, _, _ = _fixed_action_rollout(_with_delta(CFG, delta), key)
    for field in dataclasses.fields(EnvState):
        # M6.0: theta_live *carries* the knob under test, so comparing it
        # would assert delta == delta' — false by construction, and not the
        # invariant. The invariant is that every KERNEL-produced component
        # is untouched, which is exactly what the remaining fields are.
        if field.name == "theta_live":
            continue
        a, b = getattr(ref, field.name), getattr(got, field.name)
        chex.assert_trees_all_equal(a, b)
    # And the knob really did move — otherwise the loop above is vacuous.
    # (theta_live is stacked over the rollout's steps, hence the .all().)
    assert (got.theta_live.delta == delta).all()
    assert (ref.theta_live.delta == 0.0).all()


def test_delta_one_delivers_the_zero_vector_bitwise():
    """Rolled forward through the real env: with delta = 1 the aggregate is
    *exactly* 0 at every step, for any message content."""
    cfg = _with_delta(CFG, 1.0)
    key = jax.random.PRNGKey(9)
    _, state = reset(key, cfg)
    messages = jax.random.normal(key, (cfg.n_agents, MSG_DIM))
    obs, _ = reset(key, cfg)
    for t in range(6):
        agg = aggregate(messages, obs["links"])
        assert not np.asarray(agg).any(), f"nonzero delivery at t={t}"
        k = jax.random.fold_in(key, t)
        actions = jax.random.randint(k, (cfg.n_agents,), 0, N_ACTIONS, jnp.int32)
        obs, state, _, _, _ = step(k, state, actions, cfg)


def test_muted_network_reproduces_delta_one_outcomes():
    """M5.3's zeroing point is behaviourally identical to total denial: a
    policy whose emitted message is hard-zeroed produces, under delta = 0,
    the same trajectory as the unmuted policy under delta = 1 — same keys,
    same everything else. (Both deliver the zero aggregate always; nothing
    else in the env reads the graph.)"""
    net = ActorCritic(N_ACTIONS)
    k_init, k_roll = jax.random.split(jax.random.PRNGKey(13))
    params = net.init(
        k_init,
        jnp.zeros((1, CFG.obs_window, CFG.obs_window, 8), jnp.float32),
        jnp.zeros((1, 4), jnp.float32),
        jnp.zeros((1, MSG_DIM), jnp.float32),
    )

    def make_policy(mute: bool):
        def policy(key, obs, msg):
            logits, _, emitted = net.apply(params, obs["grid"], obs["vec"], msg)
            if mute:
                emitted = jnp.zeros_like(emitted)
            actions = jax.random.categorical(key, logits).astype(jnp.int32)
            return actions, emitted

        return policy

    muted_free = rollout_episode(k_roll, CFG, make_policy(True), 16)
    live_denied = rollout_episode(
        k_roll, _with_delta(CFG, 1.0), make_policy(False), 16
    )
    chex.assert_trees_all_equal(muted_free[0], live_denied[0])  # rewards
    chex.assert_trees_all_equal(
        muted_free[2]["survival_rate"], live_denied[2]["survival_rate"]
    )


def test_messages_do_not_cross_episode_boundaries():
    """rollout_episode zeroes the carry on done, so no message emitted in
    one episode can be delivered in the next."""
    cfg = dataclasses.replace(CFG, horizon=4)
    emitted_const = jnp.full((cfg.n_agents, MSG_DIM), 7.0, jnp.float32)
    seen = []

    def policy(key, obs, msg):
        seen.append(msg)
        actions = jnp.zeros((cfg.n_agents,), jnp.int32)
        return actions, emitted_const

    # Trace-free Python capture: run unjitted so `seen` collects real arrays.
    with jax.disable_jit():
        rollout_episode(jax.random.PRNGKey(1), cfg, policy, cfg.horizon + 2)
    # Step horizon (index 3) ends the episode; the aggregate at the step
    # right after it must be exactly zero even though a message was emitted.
    assert not np.asarray(seen[cfg.horizon]).any()


#: sha256 of a fixed-key / fixed-action 24-step trajectory (state fields +
#: reward + the pre-M5.0 info channels), measured at commit 0c612b6 — the
#: last commit before the comms axis existed — and reproduced bitwise by
#: this tree at delta = 0. It pins invariant #3 across the M5.0 boundary in
#: a way the in-tree delta-sweep cannot: that sweep proves delta does not
#: perturb the kernels *now*, this proves the comms draw did not shift them
#: when it was introduced. CPU-only: the digest is float32-exact and the
#: smoke exponential is not bit-identical across backends.
_PRE_COMMS_TRAJECTORY_SHA256 = (
    "7f971393cd75d371d668c81df193376edf5fd351bff1f5a66c6f619a849c3230"
)


@pytest.mark.skipif(
    jax.default_backend() != "cpu", reason="golden digest is CPU-float32-exact"
)
def test_delta_zero_reproduces_the_pre_comms_env_bitwise():
    import hashlib

    cfg = EnvConfig(
        grid_size=16, n_agents=4, horizon=32, n_food=6,
        theta=ThetaConfig(
            beta=0.49, kappa_A=0.06, kappa_B=1.0, f_weak=0.15,
            lambda_0=5e-5, lambda_load=4e-4,
        ),
    )
    key = jax.random.PRNGKey(20260728)
    k_reset, k_act, k_steps = jax.random.split(key, 3)
    actions = jax.random.randint(
        k_act, (24, cfg.n_agents), 0, N_ACTIONS, dtype=jnp.int32
    )
    _, state = reset(k_reset, cfg)
    h = hashlib.sha256()
    for i, k in enumerate(jax.random.split(k_steps, 24)):
        _, state, r, _, info = step(k, state, actions[i], cfg)
        for f in (
            "agent_pos", "agent_alive", "hazard", "smoke", "structure", "weak",
            "ep_deaths_fire", "ep_deaths_collapse", "ep_smoke_sum",
        ):
            h.update(np.asarray(getattr(state, f)).tobytes())
        h.update(np.asarray(r).tobytes())
        for kk in (
            "coupling_co_active", "seeded_ignitions", "collapse_events",
            "deaths_fire", "burnt_fraction", "masked_frac",
        ):
            h.update(np.asarray(info[kk]).tobytes())
    assert h.hexdigest() == _PRE_COMMS_TRAJECTORY_SHA256


def test_info_reports_delivery_rate_and_degree_denominators():
    """The M5.5 channel observables exist from day one, as poolable
    numerator/denominator counts (the M4.4 lesson)."""
    _, _, infos = _fixed_action_rollout(_with_delta(CFG, 0.0), jax.random.PRNGKey(2))
    assert {"links_alive", "links_in_range"} <= set(infos)
    alive = np.asarray(infos["links_alive"])
    in_range = np.asarray(infos["links_in_range"])
    assert (alive <= in_range).all()
    assert np.array_equal(alive, in_range)  # delta = 0 delivers everything
    _, _, denied = _fixed_action_rollout(
        _with_delta(CFG, 1.0), jax.random.PRNGKey(2)
    )
    assert not np.asarray(denied["links_alive"]).any()
    assert np.array_equal(
        np.asarray(denied["links_in_range"]), in_range
    )  # geometry unchanged: only the knob moved
