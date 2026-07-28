"""Comms channel T_K (Def. 7) — realized link graph and message delivery.

Phase-5 M5.0. One env step samples, for every *ordered* pair of distinct
alive agents (i, j),

    P[link i -> j alive at t] = 1[d_Cheb(x'_i, x'_j) <= R_comm] * (1 - delta)

with d_Cheb the Chebyshev distance — the crop's own metric, the same one
invariant #5's co-active test and the obs window already use.

Two design points the theory fixes and this module must not violate:

- **T_K reads positions only** (Def. 7, stated explicitly there). Never
  hazard, smoke or structure: mechanistic independence is what makes comms
  a separate load-bearing axis, even though Remark 2'/2" show the axis
  *values* interact. Hazard-coupled comms (smoke attenuating radio) is
  deliberately future work, not a shortcut available here.
- **delta = 0 is the nested model** (invariant #3). The uniforms are drawn
  unconditionally — one per ordered pair per step, the diagonal drawn and
  discarded — and compared against a probability that may be 0 or 1. Never
  gate the draw on delta. delta = 0 then recovers the deterministic range
  graph bitwise and delta = 1 the empty graph bitwise, with every other
  kernel stream untouched.

DECISION (hard range, human-ruled 2026-07-28, Q6): p_link is a hard cutoff
1[d <= R_comm], not a distance decay, so `ThetaConfig.p_link_max` is retired
rather than left as an unspecified multiplier — see config.py.

DECISION (directed links, same ruling): draws are per *ordered* pair, so for
0 < delta < 1 delivery may be asymmetric — i hears j while j does not hear i.
Physically legitimate (fading is directional) and reported as such: M5.4's
degree observable is the mean alive *out*-degree, and the delivery rate is
counted over ordered in-range pairs.

Message path (Phase-5 prompt M5.0). Agent i emits m_i in R^{MSG_DIM} at
step t; delivery happens at t+1 over the link graph realized at t+1, so
message content is strictly *pre-decision* information and there is no
intra-step fixed point. Aggregation is the masked mean over delivering
senders: permutation-invariant, the zero vector when isolated, and the
sender's own message is never self-delivered (the diagonal is excluded from
the graph, not merely zeroed afterwards).

Carry shapes (codebase-tour style, per the prompt):

    messages   float32 [n_agents, MSG_DIM]    emitted at t; lives in the
                                              training/rollout carry, never
                                              in EnvState (see types.py)
    links      bool    [n_agents, n_agents]   links[i, j]: i -> j at t+1;
                                              rides in obs, resampled each
                                              step from post-step positions
    aggregate  float32 [n_agents, MSG_DIM]    delivered to each agent at t+1

Gradient discipline (Q3 ruling, 2026-07-28): the delivered aggregate is
*stored data* in the PPO batch, so no gradient crosses the channel. See
networks.py for what that implies about the message head.
"""

import chex
import jax
import jax.numpy as jnp

# Message width (Phase-5 prompt: m in R^8, tanh-bounded).
MSG_DIM = 8


def in_range_mask(
    agent_pos: jax.Array, agent_alive: jax.Array, r_comm: float
) -> jax.Array:
    """Ordered pairs that are *eligible* for a link: both alive, i != j,
    Chebyshev distance <= R_comm.

    Deterministic given positions — consumes no PRNG. Returns bool
    [n_agents, n_agents] with mask[i, j] = "i -> j is in range".
    """
    chex.assert_shape(agent_pos, (None, 2))
    chex.assert_type(agent_alive, jnp.bool_)
    n = agent_pos.shape[0]
    d = jnp.max(jnp.abs(agent_pos[:, None, :] - agent_pos[None, :, :]), axis=-1)
    mask = (d <= r_comm) & agent_alive[:, None] & agent_alive[None, :]
    return mask & ~jnp.eye(n, dtype=jnp.bool_)


def sample_links(key: jax.Array, in_range: jax.Array, delta: float) -> jax.Array:
    """T_K (Def. 7): Bernoulli(1 - delta) thinning of the in-range graph.

    Invariant #3: the [n, n] uniforms are drawn unconditionally (including
    the discarded diagonal) and compared against 1 - delta, so key
    consumption never depends on delta, on positions, or on how many agents
    are alive. delta = 0 -> u < 1.0 holds for every u in [0, 1) -> the
    deterministic range graph; delta = 1 -> u < 0.0 never holds -> the empty
    graph. Both bitwise, no branch.
    """
    chex.assert_rank(in_range, 2)
    chex.assert_type(in_range, jnp.bool_)
    u = jax.random.uniform(key, in_range.shape, dtype=jnp.float32)
    return in_range & (u < (1.0 - delta))


def aggregate(messages: jax.Array, links: jax.Array) -> jax.Array:
    """Masked mean of delivered messages, per receiver (Phase-5 M5.0).

    agg[j] = sum_i links[i, j] * messages[i] / max(sum_i links[i, j], 1)

    Permutation-invariant in the senders (a mean over a set), the exact zero
    vector for an isolated or dead receiver, and self-delivery-free because
    `links` has no diagonal. Deterministic — consumes no PRNG.
    """
    chex.assert_rank([messages, links], [2, 2])
    chex.assert_type(links, jnp.bool_)
    chex.assert_axis_dimension(links, 0, messages.shape[0])
    w = links.astype(messages.dtype)
    total = w.T @ messages
    count = w.sum(axis=0)[:, None]
    return total / jnp.maximum(count, 1.0)
