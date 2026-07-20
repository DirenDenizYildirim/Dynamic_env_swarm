"""M3.0 eval-harness tests: fixed-seed reproducibility, per-episode row
count, checkpoint-hash guard, and CLI output files. Uses the same tiny
config values as test_ippo so make_train_fns' lru_cache is shared."""

import dataclasses
import json

import numpy as np
import pytest

from che.env.config import Config, EnvConfig, TrainConfig
from che.eval.harness import evaluate, load_params, main, summarize
from che.train.ippo import train

CFG = Config(
    env=EnvConfig(grid_size=12, n_agents=3, horizon=32, n_food=6),
    train=TrainConfig(
        n_envs=2, rollout_len=16, n_minibatches=2, n_epochs=2, ckpt_interval=2
    ),
)

EXPECTED_KEYS = {
    "episode_return",
    "completion",
    "survival_rate",
    "deaths_fire",
    "deaths_collapse",
    "mean_smoke_exposure",
    "coupling_co_active",
}


@pytest.fixture(scope="module")
def ckpt_dir(tmp_path_factory):
    d = tmp_path_factory.mktemp("m30") / "ckpt"
    train(CFG, n_updates=2, ckpt_dir=d, seed=0)
    return d


def test_hash_guard(ckpt_dir):
    params, step = load_params(ckpt_dir, CFG)
    assert step == 2
    other = dataclasses.replace(
        CFG, env=dataclasses.replace(CFG.env, n_food=7)
    )
    with pytest.raises(ValueError, match="hash mismatch"):
        load_params(ckpt_dir, other)
    with pytest.raises(ValueError, match="config_hash.txt"):
        load_params(ckpt_dir.parent / "nonexistent", CFG)


def test_allow_hash_named_legacy_only(ckpt_dir):
    """M3.0b forward-compat: allow_hashes admits exactly the named hash."""
    other = dataclasses.replace(
        CFG, env=dataclasses.replace(CFG.env, n_food=7)
    )
    # An allow-list that does not name the stored hash still rejects.
    with pytest.raises(ValueError, match="hash mismatch"):
        load_params(ckpt_dir, other, allow_hashes=("not-the-stored-hash",))
    # Naming the stored hash accepts the legacy checkpoint.
    stored = (ckpt_dir / "config_hash.txt").read_text()
    params, step = load_params(ckpt_dir, other, allow_hashes=(stored,))
    assert step == 2
    assert params is not None


def test_cli_allow_hash_provenance(ckpt_dir, tmp_path):
    """--allow-hash: guard still rejects without it; with it, the old->new
    mapping lands in the summary JSON (explicit and recorded, never silent);
    a matching hash records nothing."""
    cfg_tmpl = (
        "env:\n  grid_size: 12\n  n_agents: 3\n  horizon: 32\n  n_food: {n}\n"
        "train:\n  n_envs: 2\n  rollout_len: 16\n  n_minibatches: 2\n"
        "  n_epochs: 2\n  ckpt_interval: 2\n"
    )
    mismatch_cfg = tmp_path / "mismatch.yaml"
    mismatch_cfg.write_text(cfg_tmpl.format(n=7))
    out_npz = tmp_path / "legacy_eval.npz"
    base_args = [
        "--config", str(mismatch_cfg),
        "--ckpt-dir", str(ckpt_dir),
        "--n-episodes", "2",
        "--out-npz", str(out_npz),
    ]
    with pytest.raises(ValueError, match="hash mismatch"):
        main(base_args)
    stored = (ckpt_dir / "config_hash.txt").read_text()
    main(base_args + ["--allow-hash", stored])
    summary = json.loads(out_npz.with_suffix(".json").read_text())
    compat = summary["hash_compat"]
    assert compat["ckpt_hash"] == stored
    assert compat["current_hash"] != stored
    assert compat["allow_hash_flag"] == [stored]
    assert compat["timestamp"]  # ISO-8601 UTC stamp of the acceptance
    # Hash-matching eval records no compat row even with the flag set.
    match_cfg = tmp_path / "match.yaml"
    match_cfg.write_text(cfg_tmpl.format(n=6))
    out2 = tmp_path / "match_eval.npz"
    main([
        "--config", str(match_cfg),
        "--ckpt-dir", str(ckpt_dir),
        "--n-episodes", "2",
        "--out-npz", str(out2),
        "--allow-hash", "some-other-legacy-hash",
    ])
    summary2 = json.loads(out2.with_suffix(".json").read_text())
    assert "hash_compat" not in summary2


def test_row_count_and_reproducibility(ckpt_dir):
    params, _ = load_params(ckpt_dir, CFG)
    a = evaluate(CFG, params, n_episodes=8, seed=0)
    b = evaluate(CFG, params, n_episodes=8, seed=0)
    assert set(a) == EXPECTED_KEYS
    for name in a:
        assert a[name].shape == (8,), name
        np.testing.assert_array_equal(a[name], b[name])
    c = evaluate(CFG, params, n_episodes=8, seed=1)
    assert any(not np.array_equal(a[n], c[n]) for n in a)


def test_greedy_runs_and_summary(ckpt_dir):
    params, _ = load_params(ckpt_dir, CFG)
    g = evaluate(CFG, params, n_episodes=4, seed=0, greedy=True)
    assert g["completion"].shape == (4,)
    s = summarize(g)
    assert set(s) == EXPECTED_KEYS
    assert {"mean", "std", "q25", "median", "q75"} <= set(s["completion"])


def test_cli_writes_npz_and_json(ckpt_dir, tmp_path):
    cfg_path = tmp_path / "cfg.yaml"
    cfg_path.write_text(
        "env:\n  grid_size: 12\n  n_agents: 3\n  horizon: 32\n  n_food: 6\n"
        "train:\n  n_envs: 2\n  rollout_len: 16\n  n_minibatches: 2\n"
        "  n_epochs: 2\n  ckpt_interval: 2\n"
    )
    out_npz = tmp_path / "eval.npz"
    main(
        [
            "--config", str(cfg_path),
            "--ckpt-dir", str(ckpt_dir),
            "--n-episodes", "4",
            "--out-npz", str(out_npz),
        ]
    )
    data = np.load(out_npz)
    assert set(data.files) == EXPECTED_KEYS
    assert all(data[k].shape == (4,) for k in data.files)
    summary = json.loads(out_npz.with_suffix(".json").read_text())
    assert summary["ckpt_step"] == 2
    assert summary["n_episodes"] == 4
    assert set(summary["metrics"]) == EXPECTED_KEYS
