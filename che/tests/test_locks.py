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
# carry the pre-Phase-2 placeholder and are exempt by design.
CALIBRATED_ROLES = {"science", "gate", "theta_star"}


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
        for section in ("theta", "env"):
            for key, cname in (spec.get(section) or {}).items():
                assert cname in CONSTANTS, (
                    f"{path}:{section}.{key} references unknown constant {cname!r}"
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


def test_death_penalty_documented_state_is_the_actual_state():
    """dp = 0.5 is locked (D4) but reachable only from argv — flagged, not
    fixed, pending a human ruling. This asserts the DOCUMENTED state so the
    discrepancy cannot drift unnoticed in either direction."""
    spec = CONSTANTS["death_penalty"]
    assert spec["supplied_by"] == "cli"
    assert spec.get("discrepancy"), "the discrepancy note is the record — keep it"
    for path, cspec in CONFIGS.items():
        if not cspec.get("death_penalty_is_cli"):
            continue
        dp = load_config(REPO_ROOT / path).env.theta.death_penalty
        assert dp == pytest.approx(0.0), (
            f"{path}: death_penalty is now {dp}. If configs are meant to carry "
            "dp inline, that is the owed human ruling — update locks.yaml "
            "(supplied_by: config) and this test together."
        )


def test_comms_element_semantics_are_not_confused():
    """delta 0.0 in base configs is ELEMENT-OFF and correct; the locked
    element-ON value 1.0 belongs to theta_star configs only. Recorded
    because reading the uniform `delta: 0.0` as drift was the misdiagnosis
    the ruling explicitly corrected."""
    assert _value("delta_element_off") == pytest.approx(0.0)
    assert _value("delta_element_on") == pytest.approx(1.0)
    for path, spec in CONFIGS.items():
        want = (spec.get("theta") or {}).get("delta")
        if want is None:
            continue
        if spec.get("role") == "theta_star":
            assert want == "delta_element_on", f"{path}: theta* must be element-ON"
        else:
            assert want == "delta_element_off", (
                f"{path}: base/gate configs are element-OFF"
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
