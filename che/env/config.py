"""Frozen configuration dataclasses and the YAML loader.

theta = (beta, kappa_A, kappa_B, delta) is the stressor configuration of
Def. 1; sub-parameters follow the definitions they belong to. All configs are
frozen (hashable) so they can be passed as static arguments to jitted
functions — one compilation per config, no traced branching on parameters.

Nesting invariant (CLAUDE.md #3): kappa_A = kappa_B = delta = 0 must recover
the nested models *bitwise*. Kernels therefore always sample their uniforms
and compare against these probabilities; they never branch on whether a
parameter is zero.
"""

import dataclasses
from pathlib import Path

import yaml


@dataclasses.dataclass(frozen=True)
class ThetaConfig:
    """Stressor configuration theta and its sub-parameters (Def. 1)."""

    # Primary axes.
    beta: float = 0.35  # hazard transmissibility (Def. 3)
    kappa_A: float = 0.0  # collapse->ignition seeding prob. (Def. 5)
    kappa_B: float = 0.0  # Beer-Lambert attenuation strength (Def. 6)
    delta: float = 0.0  # comms denial level (Def. 7)
    # Hazard/smoke sub-parameters (Def. 3, Def. 6, D3).
    # M1.1: optional death penalty, Def.-2 compliant — reads only the alpha
    # transition (an X variable), never hazard/smoke/structure directly.
    death_penalty: float = 0.0  # reward -c per newly disabled agent
    iota: float = 0.0  # spontaneous ignition rate per Fuel cell
    sigma_s: float = 1.0  # smoke emission per Burning cell
    eta: float = 0.5  # smoke exponential decay rate
    # Collapse sub-parameters (Def. 5; inert until Phase 3, plumbed now).
    lambda_0: float = 0.0  # spontaneous collapse prob. per cell per step
    lambda_load: float = 0.0  # extra collapse prob. under agent load
    r_seed: int = 1  # Coupling A seeding neighborhood N_A radius
    # M3.1 weak-cell terrain (Def. 5 substrate): only weak cells can
    # collapse; lambda(g) = lambda_0 * weak(g) + lambda_load * weak(g) *
    # occupied(g). Mask generated at reset (dedicated stream), spatially
    # clustered via box-smoothing passes on uniform noise.
    f_weak: float = 0.0  # fraction of cells that are weak
    weak_smooth: int = 2  # 3x3 box-smoothing passes on the terrain noise
    # Comms sub-parameters (Def. 7; inert until Phase 5, plumbed now).
    p_link_max: float = 1.0  # p_link at zero distance
    r_comm: float = 8.0  # p_link range scale (cells)


@dataclasses.dataclass(frozen=True)
class EnvConfig:
    """Arena and task geometry. grid_size is the side length L (Sec. 3)."""

    grid_size: int = 16
    n_agents: int = 4
    horizon: int = 256
    # M1.2: obs v1 locked — k=9 egocentric crop over the 5 planes defined
    # in observation.py.
    obs_window: int = 9  # k: egocentric k x k crop, must be odd
    n_food: int = 8  # F food items for the Phase-0 foraging stub
    # M1.3: static-hazard control. Env-level *training-protocol* knob,
    # deliberately not in ThetaConfig — it is not a stressor element.
    # "frozen": burn the CA in for t_gen steps at reset, then freeze h.
    hazard_mode: str = "dynamic"  # {"dynamic", "frozen"}
    t_gen: int | None = None  # frozen burn-in CA steps; None -> horizon // 2
    theta: ThetaConfig = dataclasses.field(default_factory=ThetaConfig)

    def __post_init__(self) -> None:
        if self.obs_window % 2 != 1:
            raise ValueError(f"obs_window must be odd, got {self.obs_window}")
        if self.hazard_mode not in ("dynamic", "frozen"):
            raise ValueError(f"unknown hazard_mode: {self.hazard_mode!r}")

    @property
    def t_gen_resolved(self) -> int:
        """Burn-in length for frozen mode (M1.3 default: horizon // 2)."""
        return self.t_gen if self.t_gen is not None else self.horizon // 2


@dataclasses.dataclass(frozen=True)
class TrainConfig:
    """Training-loop configuration (fleshed out at M0.5/M0.6)."""

    n_envs: int = 2
    pop_size: int = 2
    # IPPO hyperparameters (PureJaxRL-style defaults; PBT mutates lr and
    # ent_coef per member from these initial values).
    lr: float = 3e-4
    gamma: float = 0.99
    gae_lambda: float = 0.95
    clip_eps: float = 0.2
    ent_coef: float = 0.01
    vf_coef: float = 0.5
    max_grad_norm: float = 0.5
    rollout_len: int = 128  # env steps collected per update
    n_minibatches: int = 4
    n_epochs: int = 4
    # PBT outer loop (M0.6).
    pbt_interval: int = 20  # K_pbt: updates between exploit/explore
    # Checkpointing (M0.5).
    ckpt_interval: int = 50  # K: updates between orbax checkpoints


@dataclasses.dataclass(frozen=True)
class Config:
    """Top-level bundle loaded from a YAML file."""

    env: EnvConfig
    train: TrainConfig


def load_config(path: str | Path) -> Config:
    """Load a YAML config; unknown keys raise (typo protection)."""
    with open(path) as f:
        raw = yaml.safe_load(f) or {}
    theta = ThetaConfig(**raw.get("theta", {}))
    env_kwargs = raw.get("env", {})
    env = EnvConfig(theta=theta, **env_kwargs)
    train = TrainConfig(**raw.get("train", {}))
    return Config(env=env, train=train)
