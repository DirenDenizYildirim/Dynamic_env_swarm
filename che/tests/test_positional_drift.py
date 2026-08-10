"""Render-gate positional-drift diagnostic (registrar-ruled 2026-08-10).

The render inspection found trained policies acquiring a per-training-run
residual action bias which the absorbing boundary integrates into a wall
pile-up. Not an env bug -- env geometry is symmetric and the drift direction
varies by checkpoint -- but invisible to every differenced falsifier the
project runs, because an effect present in both arms cancels exactly.

These tests cover the two adopted channels. Three groups, and the third is
the one that matters most:

1. GEOMETRY. `center_dist_sum` and `boundary_agents` mean what their names
   say, on all four edges, counting alive agents only.
2. PURITY. Both are exact functions of the returned state -- no PRNG
   (invariant #3), nothing a kernel could read back (Def. 2).
3. DETECTION. A positive control: a policy with the exact bias the diagnostic
   was built to catch must move both channels to saturation. An instrument
   that cannot see its own target is void, not passing -- the same standard
   `bars come with floors` applies to thresholds.

Chain coverage (env -> Transition -> pooled metric -> jsonl) is NOT repeated
here; `test_step_metrics.py` enumerates STEP_METRICS generically and picks
these up for free.
"""

from __future__ import annotations

import dataclasses

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from che.env.config import load_config
from che.env.env import reset, step
from che.env.types import theta_live_from, zeros_state

STAY, UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3, 4


@pytest.fixture(scope="module")
def cfg():
    return load_config("che/configs/debug.yaml")


def _benign(cfg, positions, alive=None):
    """An all-clear state with agents placed exactly where the test wants.

    `zeros_state` is all-Fuel, unweakened and intact, so nothing burns and
    nothing collapses: agents cannot die and STAY cannot be blocked. The
    geometry assertions below are therefore exact rather than probabilistic.
    """
    ecfg = cfg.env
    state = zeros_state(
        ecfg.grid_size,
        ecfg.n_agents,
        jax.random.PRNGKey(0),
        theta_live_from(ecfg.theta),
    )
    pos = jnp.asarray(positions, jnp.int32)
    assert pos.shape == (ecfg.n_agents, 2), "test places every agent"
    if alive is None:
        alive = jnp.ones((ecfg.n_agents,), jnp.bool_)
    return dataclasses.replace(state, agent_pos=pos, agent_alive=alive)


def _stay(cfg, state):
    """Step with every agent holding position; returns the info dict."""
    actions = jnp.full((cfg.env.n_agents,), STAY, jnp.int32)
    _, _, _, _, info = step(jax.random.PRNGKey(1), state, actions, cfg.env)
    return info


# --------------------------------------------------------------- 1. geometry


def test_center_distance_is_chebyshev_from_the_arena_center(cfg):
    """(L-1)/2 at the corners, 0.5 at the four cells straddling the centre.

    The centre of an even grid is a half-integer the agents straddle rather
    than a cell they occupy, so 0.5 -- not 0 -- is the floor of this channel.
    """
    ll = cfg.env.grid_size
    half = (ll - 1) / 2.0
    c = (ll - 1) // 2

    corner_cells = [[0, 0], [0, ll - 1], [ll - 1, 0], [ll - 1, ll - 1]]
    corners = _stay(cfg, _benign(cfg, corner_cells))
    assert float(corners["alive_agents"]) == cfg.env.n_agents
    assert float(corners["center_dist_sum"]) == pytest.approx(cfg.env.n_agents * half)

    middle = _stay(cfg, _benign(cfg, [[c, c], [c, c + 1], [c + 1, c], [c + 1, c + 1]]))
    assert float(middle["center_dist_sum"]) == pytest.approx(cfg.env.n_agents * 0.5)


def test_boundary_contact_fires_on_every_edge_and_only_there(cfg):
    """All four edges count; the ring one cell inside counts for none of them.

    An off-by-one that dropped an edge, or that leaked into the interior,
    would bias the wall-pile-up statistic in exactly the direction the
    diagnostic exists to measure.
    """
    ll = cfg.env.grid_size
    mid = ll // 2

    edges = _stay(cfg, _benign(cfg, [[0, mid], [ll - 1, mid], [mid, 0], [mid, ll - 1]]))
    assert float(edges["boundary_agents"]) == cfg.env.n_agents

    inside = _stay(
        cfg,
        _benign(cfg, [[1, mid], [ll - 2, mid], [mid, 1], [mid, ll - 2]]),
    )
    assert float(inside["boundary_agents"]) == 0.0


def test_dead_agents_are_counted_by_neither_channel(cfg):
    """Both channels are sums over ALIVE agents, matching their denominator.

    A corpse left on a wall would otherwise read as a live agent parked on
    it -- and the arm where that matters most, High, is the arm that loses
    the most agents.
    """
    ll = cfg.env.grid_size
    corner = [[ll - 1, ll - 1]] * cfg.env.n_agents
    alive = jnp.array([True] + [False] * (cfg.env.n_agents - 1))
    info = _stay(cfg, _benign(cfg, corner, alive=alive))

    assert float(info["alive_agents"]) == 1.0
    assert float(info["boundary_agents"]) == 1.0
    assert float(info["center_dist_sum"]) == pytest.approx((ll - 1) / 2.0)


# ----------------------------------------------------------------- 2. purity


def test_channels_are_an_exact_function_of_the_returned_state(cfg):
    """Recompute both from (agent_pos, agent_alive) alone and match bitwise.

    This is the invariant-#3 and Def.-2 statement in testable form: if the
    channels can be reconstructed from the post-step state, they carry no
    hidden PRNG draw and no dependence on anything a kernel or the reward
    could read back. Run over a real rollout so the agents actually move.
    """
    ecfg = cfg.env
    half = (ecfg.grid_size - 1) / 2.0
    key = jax.random.PRNGKey(7)
    _, state = reset(key, ecfg)

    for t in range(12):
        key, k_act, k_step = jax.random.split(key, 3)
        actions = jax.random.randint(k_act, (ecfg.n_agents,), 0, 5, jnp.int32)
        _, state, _, _, info = step(k_step, state, actions, ecfg)

        dist = np.max(np.abs(np.asarray(state.agent_pos, np.float32) - half), axis=-1)
        alive = np.asarray(state.agent_alive)
        expect_sum = float(np.where(alive, dist, 0.0).sum())
        expect_edge = float((alive & (dist >= half)).sum())
        assert float(info["center_dist_sum"]) == expect_sum, (
            f"center_dist_sum diverged from the state at t={t}"
        )
        assert float(info["boundary_agents"]) == expect_edge, (
            f"boundary_agents diverged from the state at t={t}"
        )


def test_channels_do_not_perturb_the_trajectory(cfg):
    """Same key in, same trajectory out, twice -- the channels consume no key.

    A channel that drew a uniform would break the bitwise ablation nesting
    (invariant #3) for every config at once. `test_theta_golden` is the
    cross-tree authority; this is the cheap local guard.
    """
    ecfg = cfg.env
    actions = jnp.array([DOWN, DOWN, LEFT, RIGHT][: ecfg.n_agents], jnp.int32)
    _, s0 = reset(jax.random.PRNGKey(3), ecfg)

    outs = [step(jax.random.PRNGKey(4), s0, actions, ecfg) for _ in range(2)]
    assert jnp.array_equal(outs[0][1].agent_pos, outs[1][1].agent_pos)
    assert float(outs[0][4]["center_dist_sum"]) == float(outs[1][4]["center_dist_sum"])


# -------------------------------------------------------------- 3. detection


def test_the_diagnostic_detects_the_bias_it_was_built_for(cfg):
    """Positive control: a constantly-DOWN policy saturates both channels.

    This is the effect the render inspection diagnosed -- a residual action
    bias integrated by the absorbing boundary, which is a no-op rather than a
    bounce, so the pile-up does not relax once formed. If this test can be
    made to pass by an instrument that cannot see that, the instrument is
    void and so is anything it grades.
    """
    ecfg = cfg.env
    ll = ecfg.grid_size
    half = (ll - 1) / 2.0
    key = jax.random.PRNGKey(11)
    _, state = reset(key, ecfg)
    actions = jnp.full((ecfg.n_agents,), DOWN, jnp.int32)

    info = None
    for _ in range(ll + 4):  # enough to cross the arena from any spawn row
        key, k_step = jax.random.split(key)
        _, state, _, _, info = step(k_step, state, actions, ecfg)

    alive = float(info["alive_agents"])
    assert alive > 0, "positive control lost every agent; re-seed the fixture"
    # Every survivor is pinned to the bottom row, and stays pinned.
    assert float(info["boundary_agents"]) == alive
    assert float(info["center_dist_sum"]) == pytest.approx(alive * half)


def test_a_centred_policy_leaves_both_channels_low(cfg):
    """Negative control: agents held at the centre never touch a wall.

    Without this the positive control alone is satisfied by a channel that
    reports saturation unconditionally.
    """
    ll = cfg.env.grid_size
    c = (ll - 1) // 2
    info = _stay(cfg, _benign(cfg, [[c, c]] * cfg.env.n_agents))
    assert float(info["boundary_agents"]) == 0.0
    assert float(info["center_dist_sum"]) == pytest.approx(cfg.env.n_agents * 0.5)


# ------------------------------------------------- the keep-alive set, fixed


def test_bench_keepalive_covers_every_logged_metric_table():
    """The bench's `training` probe must keep alive what the collector reads.

    Found 2026-08-10: `_training_info_keys` enumerated EP_METRICS only, so
    from 2026-08-04 -- when STEP_METRICS was added as a SECOND table -- every
    training-mode row measured an env whose newest channels XLA was free to
    delete. That is the M5.1 defect recurring one table later.

    Asserting a superset of both tables means a third table fails here rather
    than drifting silently for months.
    """
    from che.bench.throughput import _training_info_keys
    from che.train.ippo import EP_METRICS, STEP_METRICS

    keys = set(_training_info_keys())
    missing = (set(EP_METRICS) | set(STEP_METRICS)) - keys
    assert not missing, (
        f"the bench's training keep-alive set omits {sorted(missing)}, so XLA "
        "may delete that work and the row will overstate throughput."
    )


def test_the_drift_channels_carry_their_denominator_to_the_log():
    """`alive_agents` must reach the training log beside the two numerators.

    Both channels are sums over alive agents. Undenominated they fall as
    agents die and confound positional drift with mortality -- at High,
    survival moves 8.8 points between arms, which is larger than the effect
    being measured. Deleting this entry would leave the log's drift channels
    quietly uninterpretable rather than obviously broken.
    """
    from che.train.ippo import STEP_METRICS

    for name in ("center_dist_sum", "boundary_agents", "alive_agents"):
        assert name in STEP_METRICS, f"{name} dropped out of STEP_METRICS"
