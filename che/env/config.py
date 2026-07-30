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
    # kappa_B (Def. 6): Beer-Lambert attenuation strength — optical depth
    # is the product kappa_B * rho, so sweeping kappa_B alone spans the
    # whole attenuation family; (sigma_s, eta) therefore stay at their
    # long-standing values (Phase-4 prompt note: changing smoke constants
    # would change the env family for no expressive gain).
    kappa_B: float = 0.0
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
    # Comms sub-parameters (Def. 7; live from Phase 5 / M5.0).
    # DECISION (human-ruled 2026-07-28, Q6): p_link is a HARD range cutoff,
    # p = 1[d_Cheb <= r_comm] * (1 - delta), so the former `p_link_max`
    # multiplier is retired rather than left in as an unspecified knob —
    # it had no meaning under a hard cutoff and no config ever set it.
    # R_comm is LOCKED at 16 (comms_lock.md, M5.3 CLOSURE RULING
    # 2026-07-30; recorded in docs/locks.yaml, asserted by
    # che/tests/test_locks.py). M5.4 was folded into that ruling rather
    # than run, so R_comm is locked on the GEOMETRIC observable alone:
    # mean alive out-degree 2.99-3.37 at R = 16 (M5.3b Cell B, 12 agents
    # on 64^2, trained High policies) is inside the [2, 5] prior band,
    # where R = 8 measures 0.93-1.06 and misses it. Only R in {8, 16} were
    # ever measured; the {6..28} sweep was not run and P(swarm connected)
    # was never measured — both recorded as limitations of the lock, which
    # is admissible only because performance is insensitive to R_comm.
    # The default carries the locked value so it cannot be reached by argv
    # alone; configs still state it explicitly (repo-explorer ruling 1a,
    # 2026-07-31). Cost is shape-invariant in r_comm: in_range_mask builds
    # the full [n, n] Chebyshev matrix and sample_links draws [n, n]
    # uniforms unconditionally (invariant #3), so throughput figures
    # measured at 8.0 keep their meaning.
    r_comm: float = 16.0  # R_comm: hard comms range in cells (Chebyshev)


@dataclasses.dataclass(frozen=True)
class EnvConfig:
    """Arena and task geometry. grid_size is the side length L (Sec. 3)."""

    grid_size: int = 16
    n_agents: int = 4
    horizon: int = 256
    # M1.2: obs locked — k=9 egocentric crop over the planes defined in
    # observation.py.
    obs_window: int = 9  # k: egocentric k x k crop, must be odd
    # M4.1 (2026-07-24): obs v3 — v2 indicator planes gated by Coupling B
    # masking + visibility plane — is the default; v2 (D5, unmasked) and
    # v1 (mixed ordinal encodings) are restorable for archival evaluation
    # only. Schema frozen after M4.1 (Phase 5 adds message inputs, not
    # grid planes).
    obs_version: int = 3  # {1, 2, 3}
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
        if self.obs_version not in (1, 2, 3):
            raise ValueError(f"unknown obs_version: {self.obs_version!r}")

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
    # M5.1f: the pre-registered uint8 obs-storage contingency (standing rule
    # 2026-07-21), ACTIVATED. Trajectory crops are stored quantized and
    # normalized back in-network, cutting the PPO batch's dominant tensor 4x.
    # Default off so every pre-M5.1f config keeps its exact behaviour; the
    # gate/Phase-6-7 configs switch it on explicitly. Off and on are
    # different runs, never bitwise-comparable.
    #
    # CORRECTION (2026-07-29): this comment previously also claimed the
    # default preserved the *config hash*. It does not, and could not —
    # config_hash is sha256(repr(cfg)) and a frozen dataclass repr lists
    # every field, so ADDING a field moves the hash of every config
    # regardless of its default. Pre-M5.1f checkpoints therefore need
    # `--allow-hash` to evaluate or resume, which is the mechanism the
    # harness already documents for exactly this ("config-schema changes
    # move the hash of an unchanged physical config"). Stated plainly
    # because someone resuming an old checkpoint would otherwise trust a
    # guarantee that was never true.
    uint8_obs: bool = False
    # M5.1g: gradient checkpointing (rematerialization) in the PPO loss.
    # Backprop activations across the population vmap — not obs storage —
    # are the dominant term at gate scale: 98,304 agent-rows x ~18.7 KiB x
    # 12 members, doubled by the backward pass. remat recomputes the forward
    # instead of retaining it. Mathematically neutral (same hyperparameters,
    # same updates), unlike changing n_minibatches; costs compute.
    remat: bool = False
    # M5.3 utility gate: which message content reaches the aggregation
    # point. All three arms share the architecture, the parameter count and
    # the input shapes exactly — the ablation is content, not capacity.
    #   "live"     — as emitted.
    #   "zeroed"   — hard-zeroed aggregate: the channel carries nothing.
    #   "shuffled" — sender identities permuted within the step (round-2
    #                ruling item 3). The link graph and the multiset of
    #                emitted messages are untouched, so delivery pattern and
    #                marginal content distribution survive and only
    #                who-said-what is destroyed. It separates "the swarm
    #                uses sender-specific content" from "the swarm only
    #                needs connectivity or a global summary".
    # The shuffle key is derived by fold_in, never by an extra split, so all
    # three arms consume identical PRNG streams and stay CRN-paired.
    #
    # Adding this field moved every config hash again (see the uint8_obs
    # correction above). Pre-M5.3 checkpoints — the Phase-4 grid, the
    # pretask replicates, m51/m51e — need `--allow-hash` from here on.
    msg_mode: str = "live"

    def __post_init__(self) -> None:
        if self.msg_mode not in ("live", "zeroed", "shuffled"):
            raise ValueError(f"unknown msg_mode: {self.msg_mode!r}")


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
