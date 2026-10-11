"""F6a Severity explorer: P_span against beta at L = 32 / 48 / 64 (committed
estimator output), the three locked severity levels, and an ILLUSTRATIVE
synchronized fire render at each level.

Selection rule (DESIGN.md section 6, rule 3, written before rendering):
che.scripts.render_episode.rollout_frames on
che/configs/severity_{low,medium,high}.yaml,
random policy (che.train.rollout.make_random_policy), episode key
jax.random.PRNGKey(0), one episode each, all 257 states; only the hazard and
smoke layers are drawn; labelled "illustrative · random policy · episode key 0".

Calibration data: che/bench/results/phase2/estimates.npz (p_span_L*, p_span_se_L*,
beta_half); locked levels and their P_span / burnt fraction: ledger CAL-3;
beta_c(64) ~ 0.486: ledger CAL-4. No R_L logistic centre is shown (ledger O-2).

Run from the repo root (CPU, thread-capped):
  OMP_NUM_THREADS=4 ... XLA_FLAGS=--xla_cpu_multi_thread_eigen=false nice -n 15 \
  uv run python paper/figures/interactive/src/build_severity.py
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import explorer_codec as C  # noqa: E402
from common_web import (  # noqa: E402
    OUT_DATA,
    OUT_HTML,
    REPO,
    check_html,
    load_template,
    page,
)

LEVELS = [
    ("Low", "severity_low.yaml", 0.43, "calibration: P_span 0.021, burnt 1.9 %"),
    ("Medium", "severity_medium.yaml", 0.49, "calibration: P_span 0.547, burnt 19.8 %"),
    ("High", "severity_high.yaml", 0.70, "calibration: P_span 0.998, burnt 98.3 %"),
]  # CAL-3


def extract():
    sys.path.insert(0, str(REPO))
    import jax

    import che.scripts.render_episode as RE
    from che.env.config import load_config
    from che.train.rollout import make_random_policy

    out = {}
    for name, cfgf, beta, _ in LEVELS:
        cfg = load_config(str(REPO / "che/configs" / cfgf))
        assert abs(cfg.env.theta.beta - beta) < 1e-9
        frames = RE.rollout_frames(
            jax.random.PRNGKey(0), cfg.env, make_random_policy(cfg.env.n_agents)
        )
        assert len(frames) == cfg.env.horizon + 1
        hz = np.stack([f["hazard"] for f in frames])
        sm = np.stack([f["smoke"] for f in frames])
        assert sm.max() <= 1.0 + 1e-7
        out[name] = dict(hazard=hz, smoke=sm)
        np.savez_compressed(
            OUT_DATA / f"severity_{name.lower()}_frames.npz", hazard=hz, smoke=sm
        )
    return out


def load_frames():
    out = {}
    for name, *_ in LEVELS:
        p = OUT_DATA / f"severity_{name.lower()}_frames.npz"
        if not p.exists():
            return extract()
        d = np.load(p)
        out[name] = dict(hazard=d["hazard"], smoke=d["smoke"])
    return out


def build_data():
    fr = load_frames()
    est = np.load(REPO / "che/bench/results/phase2/estimates.npz")
    betas = est["betas"].tolist()
    curves = []
    for L in (32, 48, 64):
        curves.append(
            dict(
                L=L, p=est[f"p_span_L{L}"].tolist(), se=est[f"p_span_se_L{L}"].tolist()
            )
        )
    # ledger checks (CAL-3 at L = 64, CAL-4)
    p64 = dict(
        zip([round(b, 2) for b in betas], est["p_span_L64"].tolist(), strict=True)
    )
    assert (
        f"{p64[0.43]:.3f}" == "0.021"
        and f"{p64[0.49]:.3f}" == "0.547"
        and f"{p64[0.70]:.3f}" == "0.998"
    )
    assert f"{est['beta_half'][2]:.3f}" == "0.486"
    levels, panels = [], []
    for name, cfgf, beta, txt in LEVELS:
        hz, sm = fr[name]["hazard"], fr[name]["smoke"]
        q = np.round(np.clip(sm, 0, 1) * 255).astype(np.uint8)
        s = dict(
            haz0=C.b64(C.zrle(hz[0])),
            hazd=C.b64(C.hazard_diffs(hz)),
            smoke=C.b64(C.zrle(q)),
        )
        assert np.array_equal(
            C.unhazard(
                C.unzrle(C.zrle(hz[0]), hz[0].size).reshape(hz[0].shape),
                C.hazard_diffs(hz),
                hz.shape[0],
            ),
            hz,
        )
        panels.append(dict(name=name, beta=beta, **s))
        levels.append(dict(name=name, beta=beta, txt=txt))
        (OUT_DATA / f"severity_{name.lower()}_check.json").write_text(
            json.dumps(
                {
                    "config": f"che/configs/{cfgf}",
                    "rule": "rollout_frames, random policy, PRNGKey(0)",
                    "hazard_sha256": hashlib.sha256(hz.tobytes()).hexdigest(),
                    "smoke_sha256": hashlib.sha256(
                        sm.astype(np.float32).tobytes()
                    ).hexdigest(),
                    "final_non_fuel_share_this_episode": float((hz[-1] != 0).mean()),
                },
                indent=1,
            )
            + "\n"
        )
    return dict(
        betas=betas,
        curves=curves,
        levels=levels,
        panels=panels,
        L=64,
        T=int(hz.shape[0]),
        betac64="0.486",
    )


CSS = load_template("severity.css")

BODY = load_template("severity.html")

JS = load_template("severity.js")


def main():
    data = build_data()
    out = OUT_HTML / "severity_explorer.html"
    out.write_text(
        page("Severity explorer", BODY, CSS, C.JS_DECODER + JS, data), encoding="utf-8"
    )
    hits = check_html(out)
    assert not hits, hits
    print(f"{out.name}: {out.stat().st_size / 1e3:.1f} KB")


if __name__ == "__main__":
    main()
