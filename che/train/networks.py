"""Actor-critic network for the swarm.

DECISION: full parameter sharing across agents — standard for homogeneous
swarms (identical embodiment/action set), maximizes sample efficiency, and
matches the theory doc's exchangeable-agent setup. Per-agent identity can be
appended to the own-state vector later if specialization is ever needed.

Architecture: small CNN over the egocentric [k, k, 3] crop, concatenated
with the own-state vector, then separate actor/critic MLP heads.
Orthogonal init per PureJaxRL conventions.
"""

import jax
import jax.numpy as jnp
from flax import linen as nn

_ORTH = nn.initializers.orthogonal
_ZERO = nn.initializers.constant(0.0)


class ActorCritic(nn.Module):
    """(grid [..., k, k, 3], vec [..., 4]) -> (logits [..., A], value [...])."""

    n_actions: int
    hidden: int = 128

    @nn.compact
    def __call__(self, grid: jax.Array, vec: jax.Array):
        batch_shape = grid.shape[:-3]
        x = grid.reshape((-1, *grid.shape[-3:]))
        v = vec.reshape((-1, vec.shape[-1]))
        x = nn.Conv(16, (3, 3), kernel_init=_ORTH(jnp.sqrt(2)), bias_init=_ZERO)(x)
        x = nn.relu(x)
        x = nn.Conv(32, (3, 3), kernel_init=_ORTH(jnp.sqrt(2)), bias_init=_ZERO)(x)
        x = nn.relu(x)
        x = jnp.concatenate([x.reshape((x.shape[0], -1)), v], axis=-1)
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
        return (
            logits.reshape((*batch_shape, self.n_actions)),
            value.squeeze(-1).reshape(batch_shape),
        )
