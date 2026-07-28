"""Actor-critic network for the swarm, with the M5.0 message path.

DECISION: full parameter sharing across agents — standard for homogeneous
swarms (identical embodiment/action set), maximizes sample efficiency, and
matches the theory doc's exchangeable-agent setup. Per-agent identity can be
appended to the own-state vector later if specialization is ever needed.

Architecture: small CNN over the egocentric [k, k, n_planes] crop (obs v3:
7 content planes + visibility mask per M4.1; archival v2: 7, v1: 5 —
observation.py), concatenated with the own-state vector **and the delivered
message aggregate** (M5.0), then separate actor/critic MLP heads plus a
message head. Orthogonal init per PureJaxRL conventions. Channel count is
inferred from the input, so the module tracks the obs version automatically.

Message path (Phase-5 M5.0; kernel in che/env/comms.py):

    __call__(grid, vec, msg) -> (logits, value, message)

`msg` is the aggregate *delivered* to this agent at the current step —
messages its neighbours emitted one step earlier, masked-mean pooled over
the realized links (zero vector when isolated). `message` is what this agent
emits *now*, tanh-bounded to [-1, 1]^MSG_DIM, delivered at t+1. The one-step
latency is what makes message content strictly pre-decision information and
avoids an intra-step fixed point.

**Gradient discipline (Q3 ruling, human, 2026-07-28).** The delivered
aggregate is stored in the PPO batch and the loss recomputes logits from
that stored array, so *no gradient crosses the channel*. Two consequences,
stated here because they decide how M5.3's verdict must be read:

1. The message head receives zero gradient for the whole run — it stays at
   its orthogonal init. What it emits is therefore a **frozen-at-init random
   projection of trained trunk features**: the features it reads are shaped
   by the policy loss, the encoding of them is not optimized, ever.
2. Receivers *can* still learn to decode it — a random projection preserves
   information, and the input weights on the `msg` dims are trained normally.
   So "the swarm uses messages" remains falsifiable (M5.3), but "the swarm
   learned *what to say*" is out of scope by construction.

DIAL-style differentiable comms (backprop through the channel) is
pre-registered as item #1 of the M5.3 null-branch discussion, not a silent
upgrade — see docs/decision_log.md, Phase-5 pre-flight rulings round 1.
"""

import jax
import jax.numpy as jnp
from flax import linen as nn

from che.env.comms import MSG_DIM

_ORTH = nn.initializers.orthogonal
_ZERO = nn.initializers.constant(0.0)


class ActorCritic(nn.Module):
    """(grid [..., k, k, P], vec [..., 4], msg [..., MSG_DIM])
    -> (logits [..., A], value [...], message [..., MSG_DIM])."""

    n_actions: int
    hidden: int = 128
    msg_dim: int = MSG_DIM

    @nn.compact
    def __call__(self, grid: jax.Array, vec: jax.Array, msg: jax.Array):
        batch_shape = grid.shape[:-3]
        x = grid.reshape((-1, *grid.shape[-3:]))
        v = vec.reshape((-1, vec.shape[-1]))
        m = msg.reshape((-1, msg.shape[-1]))
        x = nn.Conv(16, (3, 3), kernel_init=_ORTH(jnp.sqrt(2)), bias_init=_ZERO)(x)
        x = nn.relu(x)
        x = nn.Conv(32, (3, 3), kernel_init=_ORTH(jnp.sqrt(2)), bias_init=_ZERO)(x)
        x = nn.relu(x)
        # M5.0: the delivered aggregate joins the own-state vector at the
        # trunk input — the prompt's "concatenated to the own-state vec".
        x = jnp.concatenate([x.reshape((x.shape[0], -1)), v, m], axis=-1)
        x = nn.Dense(self.hidden, kernel_init=_ORTH(jnp.sqrt(2)), bias_init=_ZERO)(x)
        x = nn.relu(x)
        actor = nn.Dense(
            self.hidden // 2, kernel_init=_ORTH(jnp.sqrt(2)), bias_init=_ZERO
        )(x)
        actor = nn.relu(actor)
        logits = nn.Dense(
            self.n_actions, kernel_init=_ORTH(0.01), bias_init=_ZERO
        )(actor)
        critic = nn.Dense(
            self.hidden // 2, kernel_init=_ORTH(jnp.sqrt(2)), bias_init=_ZERO
        )(x)
        critic = nn.relu(critic)
        value = nn.Dense(1, kernel_init=_ORTH(1.0), bias_init=_ZERO)(critic)
        # Message head: reads the shared trunk (so its input is trained),
        # never receives gradient itself (see the module docstring).
        message = jnp.tanh(
            nn.Dense(self.msg_dim, kernel_init=_ORTH(1.0), bias_init=_ZERO)(x)
        )
        return (
            logits.reshape((*batch_shape, self.n_actions)),
            value.squeeze(-1).reshape(batch_shape),
            message.reshape((*batch_shape, self.msg_dim)),
        )
