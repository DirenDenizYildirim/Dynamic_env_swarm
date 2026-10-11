"""F1 Episode explorer: one self-contained HTML file per pre-selected episode.

Input: out/data/<stem>_frames.npz written by extract_episodes.py (which
asserts frame-by-frame identity with che.scripts.render_episode.rollout_frames).
Output: out/html/explorer_<stem>.html and out/data/<stem>_codec_check.json.

Nothing here draws a survivor tally, a completion or return readout, or a
second episode. Labels are factual (policy, t, layer names).

Run from the repo root:  uv run python paper/figures/interactive/src/build_explorer.py
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import explorer_codec as C  # noqa: E402
from common_web import OUT_DATA, OUT_HTML, check_html, load_template, page  # noqa: E402

# Policy labels: plain and factual (the owner may strip them: --no-label).
EPISODES = {
    "thetastar_random_seed0": "random policy",
    "thetastar_iso_s1_T1000_ep0": "ISO policy · training seed 1 · update 1000",
    "thetastar_joint_s1_T1000_ep0": "JOINT policy · training seed 1 · update 1000",
}
# theta* values shown in the header, each with its ledger row:
# beta 0.49 (CAL-3), kappa_A 0.06 (CA-1), kappa_B 1.0 (CB-1), delta 1.0 (COM-6).
SUB = (
    "θ* (β 0.49, κ_A 0.06, κ_B 1.0, δ 1.0) · 64 × 64 cells · 12 agents · "
    "episode key 0 · one episode, illustrative"
)

DEFAULT_T = 128  # DESIGN.md section 6, rule 2


def default_agent(alive, reveal, t=DEFAULT_T) -> int:
    """DESIGN.md section 6 rule 2: lowest-index agent alive at t whose
    observation at t has at least one unseen cell; else lowest-index alive."""
    for a in range(alive.shape[1]):
        if alive[t, a] and (~reveal[t, a]).any():
            return a
    for a in range(alive.shape[1]):
        if alive[t, a]:
            return a
    return 0


def sha(a: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()


def encode(stem: str, label: str) -> tuple[dict, dict]:
    d = np.load(OUT_DATA / f"{stem}_frames.npz")
    hz, sm, food = d["hazard"], d["smoke"], d["food"].astype(bool)
    pos, alive, weak = d["pos"], d["alive"], d["weak"]
    reveal, tau = d["reveal"], d["tau"]
    seeded, coll_inc, structure = d["seeded"], d["collapse_inc"], d["structure"]
    T, L, _ = hz.shape
    NA, K = pos.shape[1], reveal.shape[2]
    assert reveal.shape == (T, NA, K, K) and tau.shape == (T, NA, K, K)
    # structure is the cumulative collapse increment (collapsed is absorbing)
    assert np.array_equal(structure.astype(bool), np.cumsum(coll_inc, 0) > 0)
    # food only disappears
    removed = np.zeros_like(food)
    removed[1:] = food[:-1] & ~food[1:]
    assert not (food[1:] & ~food[:-1]).any()
    assert pos.min() >= 0 and pos.max() < L
    q_smoke = np.round(np.clip(sm, 0, 1) * 255).astype(np.uint8)
    q_tau = (255 - np.round(np.clip(tau, 0, 1) * 255)).astype(np.uint8)
    streams = {
        "weak": np.packbits(weak.ravel()).tobytes(),
        "haz0": C.zrle(hz[0]),
        "hazd": C.hazard_diffs(hz),
        "smoke": C.zrle(q_smoke),
        "food0": np.packbits(food[0].ravel()).tobytes(),
        "foodd": C.cell_lists(removed),
        "coll": C.cell_lists(coll_inc),
        "seed": C.cell_lists(seeded),
        "pos": np.ascontiguousarray(pos.astype(np.uint8)).tobytes(),
        "alive": np.packbits(alive.ravel()).tobytes(),
        "reveal": np.packbits(reveal.ravel()).tobytes(),
        "tau": C.zrle(q_tau),
    }
    # --- Python round trip (mirror of the JS decoder) ---
    N = L * L
    assert np.array_equal(
        C.unhazard(C.unzrle(streams["haz0"], N).reshape(L, L), streams["hazd"], T), hz
    )
    assert np.array_equal(
        C.unzrle(streams["smoke"], T * N).reshape(q_smoke.shape), q_smoke
    )
    assert np.array_equal(C.uncell_lists(streams["coll"], T, L), coll_inc)
    assert np.array_equal(C.uncell_lists(streams["seed"], T, L), seeded)
    assert np.array_equal(C.uncell_lists(streams["foodd"], T, L), removed)
    assert np.array_equal(
        C.unzrle(streams["tau"], q_tau.size).reshape(q_tau.shape), q_tau
    )
    assert np.array_equal(
        np.unpackbits(np.frombuffer(streams["reveal"], np.uint8))[: reveal.size]
        .reshape(reveal.shape)
        .astype(bool),
        reveal,
    )
    a0 = default_agent(alive, reveal)
    meta = dict(
        L=int(L),
        N=int(NA),
        K=int(K),
        T=int(T),
        H=int(T - 1),
        label=label,
        sub=SUB,
        t0=DEFAULT_T,
        agent0=int(a0),
    )
    data = {"meta": meta, **{k: C.b64(v) for k, v in streams.items()}}
    # checksums the node test compares the JS decoder's output against
    check = {
        "stem": stem,
        "hazard": sha(hz.astype(np.uint8)),
        "smoke_q": sha(q_smoke),
        "collapsed": sha(np.cumsum(coll_inc, 0).astype(bool).astype(np.uint8)),
        "food": sha(food.astype(np.uint8)),
        "alive": sha(alive.astype(np.uint8)),
        "reveal": sha(reveal.astype(np.uint8)),
        "tau_q": sha(q_tau),
        "pos": sha(pos.astype(np.uint8)),
        "seeded_cells_per_frame": [int(x) for x in seeded.reshape(T, -1).sum(1)],
        "default_agent_index": int(a0),
        "stream_bytes": {k: len(v) for k, v in streams.items()},
    }
    return data, check


CSS = load_template("explorer.css")

BODY = load_template("explorer.html")

JS = load_template("explorer.js")


def build(stem: str, label: str | None) -> Path:
    data, check = encode(stem, label if label is not None else "")
    html = page(
        title="Episode explorer",
        body=BODY,
        css=CSS,
        js=C.JS_DECODER + JS,
        data=data,
    )
    out = OUT_HTML / f"explorer_{stem}.html"
    out.write_text(html, encoding="utf-8")
    check["html_bytes"] = out.stat().st_size
    (OUT_DATA / f"{stem}_codec_check.json").write_text(
        json.dumps(check, indent=1) + "\n"
    )
    hits = check_html(out)
    assert not hits, hits
    return out


def main():
    no_label = "--no-label" in sys.argv
    for stem, label in EPISODES.items():
        out = build(stem, None if no_label else label)
        print(f"{out.name}: {out.stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
