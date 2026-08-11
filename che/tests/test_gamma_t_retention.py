"""The Gamma(t) robustness window must survive on disk (T* ruling, 2026-08-11).

The plateau criterion was retired as a certification instrument and replaced
by a REQUIRED robustness reading: the fixed-budget conclusion is budget-robust
iff the sign of Gamma is stable over the FINAL HALF of training. That evidence
is only computable if updates [T/2, T] still exist when the post-unblind
Gamma(t) stage runs -- and orbax keeps only the last `max_to_keep` saves.

At the default `max_to_keep = 3` the grid would retain updates 900/950/1000
and the registered window would be UNRECOVERABLE after ~$41 of grid spend.
That is the cheap-now-impossible-later shape invariant #5 exists against.

WHAT THESE TESTS PIN, AND WHY IT IS THE RELATIONSHIP RATHER THAN THE NUMBER.
11 equals "the final half" only because T* = 1000 and ckpt_interval = 50. If
T* ever moved, 11 would silently stop meaning that, the window would shrink,
and every existing test would stay green -- the same provenance rot the T*
ruling's item 7 was issued against, one layer down. So the derivation is
asserted against the LIVE constants, not against a literal.
"""

from __future__ import annotations

import pytest
import yaml

from che.env.config import load_config
from che.scripts.m62_report import GAMMA_T_RETENTION, T_STAR
from che.scripts.make_phase6_configs import CONFIRMATORY, gamma_t_retention

CONFIRMATORY_CONFIGS = ("che/configs/p6_iso.yaml", "che/configs/p6_joint.yaml")
SECONDARY_CONFIGS = (
    "che/configs/p6_sweep_c50_p500.yaml",
    "che/configs/p6_ident_c40_p400.yaml",
)


def _raw(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


# ------------------------------------------------------------ the relationship


def test_retention_covers_the_final_half_of_training():
    """The registered window, derived from the live T* and cadence.

    This is the test that fails loudly if T* moves. It deliberately does not
    reference the number 11.
    """
    for path in CONFIRMATORY_CONFIGS:
        cfg = load_config(path)
        interval = cfg.train.ckpt_interval
        needed = T_STAR // (2 * interval) + 1
        assert cfg.train.ckpt_max_to_keep >= needed, (
            f"{path} retains {cfg.train.ckpt_max_to_keep} checkpoints at "
            f"interval {interval}, which covers the final "
            f"{(cfg.train.ckpt_max_to_keep - 1) * interval} updates. The "
            f"registered Gamma(t) window is the final half of T*={T_STAR}, "
            f"i.e. {T_STAR // 2} updates, needing {needed}. The window would "
            "be unrecoverable after the grid runs."
        )


def test_oldest_retained_checkpoint_is_at_or_before_half_of_t_star():
    """State the same fact the other way: which update does retention reach?"""
    for path in CONFIRMATORY_CONFIGS:
        cfg = load_config(path)
        oldest = T_STAR - (cfg.train.ckpt_max_to_keep - 1) * cfg.train.ckpt_interval
        assert oldest <= T_STAR // 2, (
            f"{path} reaches back only to update {oldest}; the reading rule "
            f"needs {T_STAR // 2}."
        )


def test_generator_derivation_agrees_with_the_registered_constant():
    """`gamma_t_retention()` is what writes the configs; it must match the lock."""
    assert gamma_t_retention() == GAMMA_T_RETENTION


def test_derivation_tracks_t_star_rather_than_being_a_literal():
    """Doubling T* must double the window, or the derivation is a fake."""
    assert gamma_t_retention(2000, 50) == 21
    assert gamma_t_retention(500, 50) == 6
    # A ragged window is refused rather than silently truncated.
    with pytest.raises(ValueError):
        gamma_t_retention(1010, 50)


# ------------------------------------------------------------------- the scope


@pytest.mark.parametrize("path", CONFIRMATORY_CONFIGS)
def test_confirmatory_arms_carry_the_window_in_the_config(path):
    """Reachable from a config, never from a flag -- the locks standing rule.

    R_comm was locked at 16 and lived only inside two shell scripts for a day
    because nothing checked. This is the check.
    """
    raw = _raw(path)
    assert "ckpt_max_to_keep" in raw["train"], (
        f"{path} does not set ckpt_max_to_keep, so the locked window is "
        "supplied by a dataclass default rather than by the config."
    )
    assert raw["train"]["ckpt_max_to_keep"] == GAMMA_T_RETENTION


@pytest.mark.parametrize("path", SECONDARY_CONFIGS)
def test_secondary_arms_do_not_carry_the_window(path):
    """Gamma is the ISO-vs-JOINT contrast; no secondary arm needs the storage.

    Not a cosmetic scope point: retention on all 12 protocol configs would
    multiply the grid's disk footprint for evidence no registered reading
    rule consumes.
    """
    raw = _raw(path)
    assert "ckpt_max_to_keep" not in raw["train"], (
        f"{path} is secondary but carries the Gamma(t) retention window."
    )
    assert load_config(path).train.ckpt_max_to_keep == 3


def test_confirmatory_set_matches_the_arms_gamma_is_defined_on():
    assert CONFIRMATORY == frozenset({"p6_iso", "p6_joint"})


def test_default_retention_is_unchanged_for_every_other_config():
    """The default must stay 3 so no pre-existing config's behaviour moves."""
    from che.env.config import TrainConfig

    assert TrainConfig().ckpt_max_to_keep == 3
    assert load_config("che/configs/debug.yaml").train.ckpt_max_to_keep == 3
