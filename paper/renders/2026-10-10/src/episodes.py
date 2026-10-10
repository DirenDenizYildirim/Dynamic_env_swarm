"""The three pre-selected episodes of the 2026-09-27 renders, and the one way
to roll them out.

Nothing here chooses an episode. The table below restates the 2026-09-27
selection rule (paper/renders/2026-09-27/README.md) as constants: theta*
config, episode key 0, stochastic actions, seed 1 of each confirmatory arm
at its latest checkpoint (step 1000), plus the random policy on the same key.

The trajectory comes from the ORIGINAL renderer's own rollout function,
`che.scripts.render_episode.rollout_frames`, called unmodified with the same
inputs as `render_episode.main()` builds for the README commands. That
function's frame dict carries hazard, smoke, food, agent positions and
aliveness but not the structural state, so `tapped_rollout` records the
`EnvState` the original code already produces: it wraps the module's
`reset` and `jax.jit` so that each returned state is appended to a list and
handed back unchanged. The jitted function is `jax.jit` of the original
lambda; no argument or return value is altered. `check_identity.py` checks
that the tap changes nothing (tapped vs untapped digests, and a redraw of the
tapped frames with the original draw code against the committed GIFs).

Imports `che` read-only; nothing under `che/` is modified.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_ROOT = HERE.parent  # paper/renders/2026-10-10
REPO = OUT_ROOT.parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import jax  # noqa: E402
import numpy as np  # noqa: E402

import che.scripts.render_episode as RE  # noqa: E402
from che.env.config import load_config  # noqa: E402
from che.eval.harness import load_params, make_policy_fn  # noqa: E402
from che.train.rollout import make_random_policy  # noqa: E402

# --- the selection rule of 2026-09-27, restated (unchanged) ----------------
CONFIG = "che/configs/theta_star_holdout.yaml"  # relative to the repo root,
# exactly as the README commands pass it
EPISODE_SEED = 0  # --seed 0: the episode key, jax.random.PRNGKey(0)
GREEDY = False  # no --greedy: actions sampled as the eval harness does
EXPECTED_CKPT_STEP = 1000  # T* = 1000, the latest step in each archive
CKPT_DIR = "che/bench/results/phase6/g1_conf_5090"
SHA_FILE = f"{CKPT_DIR}/SHA256_CKPT.txt"

EPISODES = (
    {
        "stem": "thetastar_random_seed0",
        "label": "random policy",
        "archive": None,
    },
    {
        "stem": "thetastar_iso_s1_T1000_ep0",
        "label": "ISO, seed 1",
        "archive": "ckpt_iso_s1.tar.zst",
        "archive_sha256": (
            "0fc9fd0c6bb84a09a9fdacfd80e24f85339a0d3d3858f072b0852a4466cf3b5a"
        ),
        "train_hash": "b63fc2d6764c7ffe",  # --allow-hash, per the README
    },
    {
        "stem": "thetastar_joint_s1_T1000_ep0",
        "label": "JOINT, seed 1",
        "archive": "ckpt_joint_s1.tar.zst",
        "archive_sha256": (
            "64c49ef8fc8c28b6234b4e3ed03812967f15beb49eadcbb31feff5c38ec19e61"
        ),
        "train_hash": "da6617b402b08b9b",
    },
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def verify_archive(ep: dict) -> dict:
    """sha256 of the archive == README constant == SHA256_CKPT.txt entry."""
    archive = REPO / CKPT_DIR / ep["archive"]
    got = sha256_file(archive)
    listed = {}
    for line in (REPO / SHA_FILE).read_text().splitlines():
        parts = line.split()
        if len(parts) == 2:
            listed[Path(parts[1]).name] = parts[0]
    ok = got == ep["archive_sha256"] == listed.get(ep["archive"])
    if not ok:
        raise SystemExit(
            f"archive hash check FAILED for {ep['archive']}: computed {got}, "
            f"README {ep['archive_sha256']}, SHA256_CKPT.txt "
            f"{listed.get(ep['archive'])}"
        )
    return {
        "archive": f"{CKPT_DIR}/{ep['archive']}",
        "sha256": got,
        "matches_SHA256_CKPT_txt": True,
        "matches_2026_09_27_README": True,
    }


def extract_archive(ep: dict, scratch: Path) -> Path:
    """Extract the verified archive into its own scratch directory."""
    dest = scratch / ep["stem"]
    dest.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["tar", "--zstd", "-xf", str(REPO / CKPT_DIR / ep["archive"]), "-C", str(dest)],
        check=True,
    )
    ckpt_dir = dest / ep["archive"].removesuffix(".tar.zst")
    stored = (ckpt_dir / "config_hash.txt").read_text()
    if stored != ep["train_hash"]:
        raise SystemExit(f"training hash {stored!r} != README {ep['train_hash']!r}")
    return ckpt_dir


def build(ep: dict, scratch: Path | None):
    """(ecfg, policy, provenance), exactly as render_episode.main() builds
    them for the README commands (no theta overrides were passed there)."""
    if Path.cwd().resolve() != REPO:
        raise SystemExit(
            f"run from the repo root ({REPO}): the config path "
            "is relative, as in the README commands"
        )
    cfg = load_config(CONFIG)
    ecfg = cfg.env
    prov = {"config": CONFIG, "seed": EPISODE_SEED, "greedy": GREEDY}
    if ep["archive"] is None:
        policy = make_random_policy(ecfg.n_agents)
        prov["policy"] = "random (che.train.rollout.make_random_policy)"
    else:
        prov["checkpoint"] = verify_archive(ep)
        ckpt_dir = extract_archive(ep, scratch)
        params, step = load_params(ckpt_dir, cfg, allow_hashes=(ep["train_hash"],))
        if int(step) != EXPECTED_CKPT_STEP:
            raise SystemExit(f"restored step {step} != {EXPECTED_CKPT_STEP}")
        policy = make_policy_fn(cfg, params, greedy=GREEDY)
        prov["allow_hash"] = [ep["train_hash"]]
        prov["restored_step"] = int(step)
    return ecfg, policy, prov


class _JitTap:
    """Stands in for the `jax` module inside render_episode for one call.
    Every attribute is the real one, except that `jit(f)` returns the real
    `jax.jit(f)` wrapped so that its output tuple is recorded and returned
    unchanged."""

    def __init__(self, real, sink):
        self._real, self._sink = real, sink

    def __getattr__(self, name):
        return getattr(self._real, name)

    def jit(self, fun, *args, **kwargs):
        jitted = self._real.jit(fun, *args, **kwargs)

        def tapped(*a):
            out = jitted(*a)
            self._sink.append({"state": out[1], "info": out[4]})
            return out

        return tapped


@contextmanager
def _tap(sink: list):
    real_jax, real_reset = RE.jax, RE.reset

    def reset_tap(key, cfg):
        obs, state = real_reset(key, cfg)
        sink.append({"state": state, "info": None})
        return obs, state

    RE.jax, RE.reset = _JitTap(real_jax, sink), reset_tap
    try:
        yield
    finally:
        RE.jax, RE.reset = real_jax, real_reset


def untapped_rollout(ecfg, policy) -> list[dict]:
    """The original renderer's rollout, nothing attached."""
    return RE.rollout_frames(jax.random.PRNGKey(EPISODE_SEED), ecfg, policy)


def tapped_rollout(ecfg, policy) -> tuple[list[dict], list[dict]]:
    """The original renderer's rollout plus the EnvState it produced at every
    frame (t = 0 from reset, then one per step). Asserts that the tapped
    states and the original frame dicts agree exactly on every shared array."""
    sink: list[dict] = []
    with _tap(sink):
        frames = RE.rollout_frames(jax.random.PRNGKey(EPISODE_SEED), ecfg, policy)
    if len(sink) != len(frames):
        raise AssertionError(
            f"tap recorded {len(sink)} states for {len(frames)} frames"
        )
    states = []
    for fr, rec in zip(frames, sink, strict=True):
        s = rec["state"]
        st = {
            "t": int(s.t),
            "hazard": np.asarray(s.hazard),
            "smoke": np.asarray(s.smoke),
            "structure": np.asarray(s.structure),
            "weak": np.asarray(s.weak),
            "food": np.asarray(s.food),
            "agent_pos": np.asarray(s.agent_pos),
            "agent_alive": np.asarray(s.agent_alive),
            "info": None
            if rec["info"] is None
            else {
                k: np.asarray(v).item()
                for k, v in rec["info"].items()
                if np.asarray(v).ndim == 0
            },
        }
        for a, b in (
            ("hazard", "hazard"),
            ("smoke", "smoke"),
            ("food", "food"),
            ("pos", "agent_pos"),
            ("alive", "agent_alive"),
        ):
            x, y = fr[a], st[b]
            if x.dtype != y.dtype or x.shape != y.shape or not np.array_equal(x, y):
                raise AssertionError(f"t={fr['t']}: frame[{a}] != state.{b}")
        if fr["t"] != st["t"]:
            raise AssertionError("frame/state time mismatch")
        states.append(st)
    return frames, states


def _digest(named: list[tuple[str, np.ndarray]]) -> str:
    h = hashlib.sha256()
    for name, a in named:
        a = np.ascontiguousarray(a)
        h.update(f"{name}|{a.dtype.str}|{a.shape}|".encode())
        h.update(a.tobytes())
    return h.hexdigest()


def frame_digest(fr: dict) -> str:
    """Digest of the arrays rollout_frames' own frame dict carries."""
    return _digest(
        [
            ("hazard", fr["hazard"]),
            ("smoke", fr["smoke"]),
            ("food", fr["food"]),
            ("agent_pos", fr["pos"]),
            ("agent_alive", fr["alive"]),
        ]
    )


def state_digest(st: dict) -> str:
    """Digest of the full drawn state, structure layers included."""
    return _digest(
        [
            (k, st[k])
            for k in (
                "hazard",
                "smoke",
                "structure",
                "weak",
                "food",
                "agent_pos",
                "agent_alive",
            )
        ]
    )


def chain(digests: list[str]) -> str:
    """One sha256 over the ordered per-frame digests."""
    return hashlib.sha256("\n".join(digests).encode()).hexdigest()
