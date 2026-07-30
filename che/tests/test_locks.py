"""Locks are enforced by test, not by memory (repo-explorer ruling 1c,
human-issued 2026-07-31; transcribed in docs/decision_log.md).

`docs/locks.yaml` is the single machine-readable source for every locked
constant. These tests assert that the configs and the `che/env/config.py`
dataclass defaults agree with it, and — the part that catches the defect
that motivated the ruling — that locked values are written EXPLICITLY in
the configs that must carry them rather than inherited from a default or
supplied by argv.

Origin: R_comm was locked at 16 in comms_lock.md on 2026-07-30 and stayed
unreachable from any config for a day. ThetaConfig.r_comm defaulted to 8.0,
no YAML set it, and the locked geometry existed only as `--r-comm 16`
inside two shell scripts. Nothing failed, because nothing checked.

Pure YAML + dataclass work: no JAX compute, no PRNG, runs in
JAX_DISABLE_JIT=1 in well under a second.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest
import yaml

from che.env.config import EnvConfig, ThetaConfig, load_config

REPO_ROOT = Path(__file__).resolve().parents[2]
LOCKS_PATH = REPO_ROOT / "docs" / "locks.yaml"


def _locks() -> dict:
    with open(LOCKS_PATH) as f:
        return yaml.safe_load(f)


LOCKS = _locks()
CONSTANTS = LOCKS["constants"]
CONFIGS = LOCKS["configs"]

# Roles whose beta must be a calibrated severity — archival configs still
# carry the pre-Phase-2 placeholder and are exempt by design, and
# theta_star_pending carries a sentinel that does not load at all.
CALIBRATED_ROLES = {"science", "gate", "joint"}
# Roles whose comms element is ON (delta = 1.0) rather than OFF.
ELEMENT_ON_ROLES = {"joint", "theta_star_pending"}


def _value(name: str):
    """Resolve a constant name to its locked value."""
    assert name in CONSTANTS, f"{name!r} is not registered in docs/locks.yaml"
    return CONSTANTS[name]["value"]


def _raw(path: str) -> dict:
    with open(REPO_ROOT / path) as f:
        return yaml.safe_load(f) or {}


def _enforced_configs() -> list[str]:
    return [p for p, spec in CONFIGS.items() if "theta" in spec or "env" in spec]


# --------------------------------------------------------------- registry


def test_locks_file_is_well_formed():
    """Every constant carries a value key and a provenance source."""
    assert LOCKS["version"] == 1
    for name, spec in CONSTANTS.items():
        assert "value" in spec, f"{name} has no value"
        assert spec.get("source"), f"{name} has no provenance source"
        assert "locked" in spec, f"{name} does not say whether it is locked"


def test_every_config_in_the_tree_is_registered():
    """A new config cannot appear unregistered — that is how R_comm hid."""
    on_disk = {
        f"che/configs/{p.name}"
        for p in (REPO_ROOT / "che" / "configs").glob("*.yaml")
    }
    unregistered = on_disk - set(CONFIGS)
    assert not unregistered, (
        f"configs present but absent from docs/locks.yaml: {sorted(unregistered)}. "
        "Register them (role + enforced keys) in the same commit that adds them."
    )
    missing = set(CONFIGS) - on_disk
    assert not missing, f"registered in locks.yaml but not on disk: {sorted(missing)}"


def test_referenced_constants_all_exist():
    """Typos in locks.yaml must fail loudly rather than silently skip."""
    for path, spec in CONFIGS.items():
        for section in ("theta", "env", "raw_theta"):
            for key, cname in (spec.get(section) or {}).items():
                assert cname in CONSTANTS, (
                    f"{path}:{section}.{key} references unknown constant {cname!r}"
                )
        if "pending_constant" in spec:
            assert spec["pending_constant"] in CONSTANTS


def test_no_locked_constant_is_reachable_only_from_argv():
    """The class-level regression test for the whole ruling.

    r_comm was locked and reachable only via `--r-comm 16`; death_penalty
    was locked (D4) and reachable only via `--death-penalty 0.5`. Both are
    now config-supplied. If a future lock lands as `supplied_by: cli`, this
    fails and the ruling gets re-litigated on purpose.
    """
    argv_only = [
        name
        for name, spec in CONSTANTS.items()
        if spec.get("locked") and spec.get("supplied_by") == "cli"
    ]
    assert not argv_only, (
        f"locked constants reachable only from argv: {argv_only}. A locked "
        "value must be reachable from a config (CLAUDE.md: locks are "
        "enforced by test, not by memory)."
    )


# ---------------------------------------------------------------- defaults


@pytest.mark.parametrize("field,cname", sorted(LOCKS["defaults"]["theta"].items()))
def test_theta_dataclass_defaults_match_locks(field, cname):
    """The default carries the locked value, so argv is not the only path."""
    assert getattr(ThetaConfig(), field) == pytest.approx(_value(cname))


@pytest.mark.parametrize("field,cname", sorted(LOCKS["defaults"]["env"].items()))
def test_env_dataclass_defaults_match_locks(field, cname):
    assert getattr(EnvConfig(), field) == pytest.approx(_value(cname))


# ----------------------------------------------------------------- configs


@pytest.mark.parametrize("path", _enforced_configs())
def test_config_values_match_locks(path):
    """Loaded config agrees with the registry on every enforced key."""
    cfg = load_config(REPO_ROOT / path)
    spec = CONFIGS[path]
    for key, cname in (spec.get("theta") or {}).items():
        got = getattr(cfg.env.theta, key)
        assert got == pytest.approx(_value(cname)), (
            f"{path}: theta.{key} = {got}, locks.yaml says {cname} = "
            f"{_value(cname)} (source: {CONSTANTS[cname]['source']})"
        )
    for key, cname in (spec.get("env") or {}).items():
        got = getattr(cfg.env, key)
        assert got == pytest.approx(_value(cname)), (
            f"{path}: env.{key} = {got}, locks.yaml says {cname} = {_value(cname)}"
        )


@pytest.mark.parametrize("path", _enforced_configs())
def test_locked_values_are_written_explicitly_not_inherited(path):
    """THE ANTI-INHERITANCE ASSERTION — the defect that motivated the rule.

    A locked value that only a dataclass default supplies is one edit away
    from silently changing every result that reads it. Keys listed under
    `explicit:` must appear in the config's own theta block.
    """
    raw_theta = _raw(path).get("theta", {})
    for key in CONFIGS[path].get("explicit", []):
        assert key in raw_theta, (
            f"{path}: theta.{key} is locked but not written in the file — it "
            "would be inherited from the dataclass default. Write it out."
        )


@pytest.mark.parametrize("path", _enforced_configs())
def test_beta_is_a_calibrated_severity(path):
    """Tripwire: an invented severity cannot enter quietly.

    beta_holdout is null until the Phase-6 entry gate fixes AND calibrates
    it (Def. 8 requires a held-out severity for theta*). Until then the only
    admissible betas are the three Phase-2 locked values.
    """
    if CONFIGS[path].get("role") not in CALIBRATED_ROLES:
        pytest.skip("archival config — pre-Phase-2 placeholder beta by design")
    admissible = {_value(n) for n in ("beta_low", "beta_medium", "beta_high")}
    holdout = _value("beta_holdout")
    if holdout is not None:
        admissible.add(holdout)
    beta = load_config(REPO_ROOT / path).env.theta.beta
    assert beta in [pytest.approx(v) for v in admissible], (
        f"{path}: beta = {beta} is not a calibrated severity {sorted(admissible)}. "
        "A held-out beta must be calibrated and registered as beta_holdout in "
        "docs/locks.yaml first (CLAUDE.md: numbers enter derived or measured)."
    )


def test_death_penalty_is_now_reachable_from_config():
    """D4's dp = 0.5 went inline 2026-07-31 (round-2 ruling).

    No past run changed: every Phase-3/4/5 script passes `--death-penalty
    0.5`, so the override sets the value it always set. What changed is
    that a bare `--config severity_*.yaml` run no longer silently runs at
    0.0, i.e. no longer silently violates D4.
    """
    assert CONSTANTS["death_penalty"]["supplied_by"] == "config"
    locked = _value("death_penalty")
    for path in (
        "che/configs/severity_low.yaml",
        "che/configs/severity_medium.yaml",
        "che/configs/severity_high.yaml",
    ):
        dp = load_config(REPO_ROOT / path).env.theta.death_penalty
        assert dp == pytest.approx(locked), f"{path}: dp = {dp}, D4 locks {locked}"


def test_comms_element_semantics_are_not_confused():
    """delta 0.0 in base configs is ELEMENT-OFF and correct; the locked
    element-ON value 1.0 belongs to the joint_* and theta_star configs.
    Recorded because reading the uniform `delta: 0.0` as drift was the
    misdiagnosis the round-1 ruling explicitly corrected."""
    assert _value("delta_element_off") == pytest.approx(0.0)
    assert _value("delta_element_on") == pytest.approx(1.0)
    for path, spec in CONFIGS.items():
        theta = (spec.get("theta") or {}) | (spec.get("raw_theta") or {})
        want = theta.get("delta")
        if want is None:
            continue
        if spec.get("role") in ELEMENT_ON_ROLES:
            assert want == "delta_element_on", (
                f"{path}: role {spec['role']} is all-elements-ON"
            )
        else:
            assert want == "delta_element_off", (
                f"{path}: base/gate configs are element-OFF"
            )


# --------------------------------------------------- theta*, held out


def _pending_configs() -> list[str]:
    return [p for p, s in CONFIGS.items() if s.get("role") == "theta_star_pending"]


@pytest.mark.parametrize("path", _pending_configs())
def test_pending_config_does_not_load(path):
    """theta* is registered but NOT runnable, and that is the design.

    Present-and-loud beats absent: an absent theta* config would silently
    inherit the pre-Phase-2 placeholder beta 0.35 the moment somebody wrote
    one, which is the failure mode this whole registry exists to prevent.
    """
    with pytest.raises(ValueError, match="placeholder"):
        load_config(REPO_ROOT / path)


@pytest.mark.parametrize("path", _pending_configs())
def test_pending_config_has_every_other_lock_written_out(path):
    """Only the owed value may be a sentinel — everything else is locked
    and explicit, checked from the raw YAML since the config cannot load."""
    spec = CONFIGS[path]
    raw_theta = _raw(path).get("theta", {})
    for key, cname in (spec.get("raw_theta") or {}).items():
        assert key in raw_theta, f"{path}: theta.{key} is locked but not written"
        assert raw_theta[key] == pytest.approx(_value(cname)), (
            f"{path}: theta.{key} = {raw_theta[key]}, locks.yaml says {cname} = "
            f"{_value(cname)} (source: {CONSTANTS[cname]['source']})"
        )


@pytest.mark.parametrize("path", _pending_configs())
def test_pending_key_matches_an_unmeasured_constant(path):
    """The sentinel and the registry must agree that the value is owed.

    Filling in one without the other is exactly the drift this catches: a
    number in the YAML with `value: null` still in locks.yaml, or vice
    versa.
    """
    spec = CONFIGS[path]
    key, cname = spec["pending_key"], spec["pending_constant"]
    raw_value = _raw(path).get("theta", {}).get(key)
    registered = CONSTANTS[cname]["value"]
    if registered is None:
        assert isinstance(raw_value, str), (
            f"{path}: {cname} is still null in docs/locks.yaml, so theta.{key} "
            f"must remain a sentinel — found {raw_value!r}. Calibrate and "
            "register the value before writing it here."
        )
        assert CONSTANTS[cname].get("owed_by"), (
            f"{cname} is unmeasured but does not say which milestone owes it"
        )
    else:
        assert raw_value == pytest.approx(registered), (
            f"{path}: theta.{key} = {raw_value!r} but docs/locks.yaml "
            f"registers {cname} = {registered}. Update them together."
        )


def test_r_comm_reachable_without_argv():
    """The regression test for the defect itself: a config loaded with no
    command-line override must produce the locked geometry."""
    locked = _value("r_comm")
    assert ThetaConfig().r_comm == pytest.approx(locked)
    for path in ("che/configs/severity_medium.yaml", "che/configs/severity_high.yaml"):
        assert load_config(REPO_ROOT / path).env.theta.r_comm == pytest.approx(locked)
    # And the override path still works, unchanged.
    overridden = dataclasses.replace(ThetaConfig(), r_comm=8.0)
    assert overridden.r_comm == pytest.approx(8.0)
