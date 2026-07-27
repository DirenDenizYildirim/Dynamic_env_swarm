"""M4.3 Coupling-B (kappa_B) calibration engine (phase4_prompt.md).

Measures the three M4.3 lock observables over a kappa_B candidate grid,
at reference scale (64^2, 12 agents, horizon 256, obs v3) with Coupling A
live at its locked values — the severity YAMLs are loaded directly, so
the calibration cannot drift from the training configs:

- ``masked_frac`` (Medium, alive agents, fire-active steps) — band
  [0.15, 0.45]: perception meaningfully degraded, not blind;
- ``detection`` = P(a Burning cell at crop distance 3 is revealed) —
  band [0.4, 0.7];
- ``q`` from the E2C micro-env (`che.env.e2c`) — band [0.3, 0.7], the
  partial-information regime where Thm. 1 says the coupling bites.

**One rollout per severity, all candidates evaluated on its states**
(CRN). For the random policy this is exact rather than merely paired:
Coupling B lives in the observation kernel only, so kappa_B cannot
perturb an obs-blind trajectory (invariant #3, proven in
`test_kappa_b_cannot_perturb_state_trajectories`). For a probe policy
the trajectory *would* react to kappa_B; DECISION: the state
distribution is held fixed at the probe's own training kappa_B so the
sweep stays paired — re-rolling per candidate would confound the
observable's kappa_B dependence with the policy's reaction to it, and
the observables are properties of the *visited states*.

Both observables are computed as **expectations**, not realized draws:
masked_frac is the mean of (1 - tau) over crop cells, which is exactly
the expectation of the env's `masked_frac` info channel, and detection
is the mean of tau over Burning ring cells, which is exactly the reveal
probability. Same estimand, no Bernoulli noise.

`transmittance` is called for every candidate (vmapped over kappa_B —
the shared function takes it as a traced multiplier), never re-derived:
M4.1 locked it as THE ONE code path and the M4.2 handshake is only
meaningful if the calibration measures the same kernel.

Finding-1 obligation (M4.2 ruling item 2): `endpoint_sampled_fraction`
confirms in-code that the distance-3 detection ring sits inside the
quadrature-sampled regime, i.e. that a single-cell source there is
actually occludable. Reported in the JSON and quoted in
`kappa_b_lock.md` rather than left implicit.

CLI (writes che/bench/results/phase4/m43/coupling_b_calibration.json):

    nice -n 19 uv run python -m che.calibration.coupling_b
    uv run python -m che.calibration.coupling_b \
        --probe-ckpt medium=path/to/ckpt --probe-kappa-B 0.5
"""

import argparse
import dataclasses
import json
import subprocess
import time
from pathlib import Path

import jax
import jax.numpy as jnp
import numpy as np

from che.env.config import Config, EnvConfig, load_config
from che.env.e2c import KAPPA_GRID as E2C_REPORTED_GRID  # noqa: F401 (provenance)
from che.env.e2c import e2c_config, tau_profile
from che.env.env import N_ACTIONS, reset, step
from che.env.observation import observe, transmittance
from che.env.types import BURNING, FUEL

SEVERITY_CONFIGS = {
    "low": "che/configs/severity_low.yaml",
    "medium": "che/configs/severity_medium.yaml",
    "high": "che/configs/severity_high.yaml",
}

# Candidate grid (>= 5 required). Deliberately wide and dense: evaluating
# a candidate costs one extra `transmittance` call on states that are
# already being visited, so resolution is nearly free — and the lock
# hinges on where three bands intersect, which a coarse grid would blur.
KAPPA_CANDIDATES = (0.05, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0)

# Detection band probe distance (phase prompt: "crop distance 3").
# DECISION: Euclidean distance rounded to 3, i.e. the ring
# |dist - 3| < 0.5 — the crop's own metric is Euclidean (transmittance
# weights optical depth by it), so a Chebyshev ring would mix true
# distances 3.0-4.24 and blur the band.
DETECTION_DIST = 3.0
DETECTION_HALFWIDTH = 0.5

# Reference kappa_B for the "carrier" test behind masked_frac's ceiling:
# a crop cell can be masked at all iff its ray carries optical depth
# D = dist * mean_rho > 0. Testing tau < 1 at a candidate kappa_B would
# make the answer grid-dependent (float32 rounds exp(-D*kappa_B) to 1.0
# for small D*kappa_B); at 1e6 the test resolves D > ~1e-13, i.e. D > 0.
CEILING_KAPPA = 1.0e6

# Bands (phase4_prompt.md M4.3).
BANDS = {
    "masked_frac_medium": (0.15, 0.45),
    "detection_medium": (0.4, 0.7),
    "e2c_q": (0.3, 0.7),
}


def ring_mask(k: int) -> jax.Array:
    """[k, k] float mask of crop cells at Euclidean distance ~ 3."""
    r = k // 2
    span = jnp.arange(-r, r + 1, dtype=jnp.float32)
    dist = jnp.sqrt(span[:, None] ** 2 + span[None, :] ** 2)
    return (jnp.abs(dist - DETECTION_DIST) < DETECTION_HALFWIDTH).astype(jnp.float32)


def endpoint_sampled_fraction(k: int, kappa_B: float = 5.0) -> float:
    """Share of detection-ring cells that a single-cell smoke source at
    that cell can actually occlude (M4.2 Finding 1 regime check).

    The n_quad midpoint samples miss the ray's endpoint beyond axis
    distance ~4, and an isolated source there reads tau == 1 at any
    kappa_B. The detection band is only measurable where this returns
    1.0 — asserted by the M4.3 test and recorded in the lock doc.
    """
    r = k // 2
    grid = 2 * k + 1
    centre = grid // 2
    pos = jnp.array([[centre, centre]], jnp.int32)
    ring = np.asarray(ring_mask(k))
    occludable, total = 0, 0
    for i in range(k):
        for j in range(k):
            if not ring[i, j]:
                continue
            total += 1
            smoke = (
                jnp.zeros((grid, grid), jnp.float32)
                .at[centre + i - r, centre + j - r]
                .set(1.0)
            )
            tau = transmittance(smoke, pos, kappa_B=kappa_B, k=k)
            occludable += int(float(tau[0, i, j]) < 1.0)
    return occludable / max(total, 1)


def _random_policy(key: jax.Array, obs: dict, n_agents: int) -> jax.Array:
    del obs
    return jax.random.randint(key, (n_agents,), 0, N_ACTIONS, dtype=jnp.int32)


def episode_observables(
    key: jax.Array,
    cfg: EnvConfig,
    kappas: jax.Array,
    policy=None,
) -> dict[str, jax.Array]:
    """One episode; per-candidate masked_frac and detection accumulators.

    `policy(key, obs) -> actions` (eval-harness PolicyFn); None = random.
    """
    k = cfg.obs_window
    ring = ring_mask(k)
    # Unmasked content planes come from the archival v2 path on the same
    # state — production code, no key, plane 0 is the burning indicator.
    cfg_v2 = dataclasses.replace(cfg, obs_version=2)
    k_reset, k_run = jax.random.split(key)
    obs0, state0 = reset(k_reset, cfg)

    def body(carry, key_t):
        (
            obs,
            state,
            masked_sum,
            fire_steps,
            det_num,
            det_den,
            ceiling_sum,
            exposed_sum,
            masked_exp_sum,
            exp_agents,
        ) = carry
        k_act, k_step = jax.random.split(key_t)
        if policy is None:
            actions = _random_policy(k_act, obs, cfg.n_agents)
        else:
            actions = policy(k_act, obs)
        obs_new, state_new, _, _, _ = step(k_step, state, actions, cfg)

        # tau per candidate on the post-step state (Prop.-1 order).
        taus = jax.vmap(
            lambda kb: transmittance(
                state_new.smoke, state_new.agent_pos, kappa_B=kb, k=k
            )
        )(kappas)  # [n_cand, n_agents, k, k]
        alive = state_new.agent_alive
        n_alive = jnp.maximum(alive.sum(dtype=jnp.float32), 1.0)

        # E[masked_frac]: mean over alive agents of the masked crop share.
        per_agent = (1.0 - taus).mean(axis=(-2, -1))  # [n_cand, n_agents]
        masked = jnp.where(alive[None, :], per_agent, 0.0).sum(-1) / n_alive
        fire_active = (state_new.hazard == BURNING).any()
        masked_sum = masked_sum + jnp.where(fire_active, masked, 0.0)
        fire_steps = fire_steps + fire_active.astype(jnp.float32)

        # Detection: mean tau over Burning cells on the distance-3 ring.
        burning = observe(state_new, cfg_v2)["grid"][..., 0]  # [n_agents,k,k]
        w = burning * ring[None] * alive[:, None, None].astype(jnp.float32)
        det_num = det_num + (taus * w[None]).sum(axis=(-3, -2, -1))
        det_den = det_den + w.sum()

        # Why masked_frac lands where it does (M4.3 diagnostic). A crop
        # cell can only ever be masked if its ray carries optical depth
        # (D = dist * mean_rho > 0, i.e. tau < 1 at some kappa_B); cells
        # with no smoke on the ray are transparent at *every* kappa_B.
        # The share of such "carrier" cells is therefore the **ceiling**
        # masked_frac approaches as kappa_B -> infinity, and it is set by
        # geometry and where the swarm stands, not by the coupling.
        carrier = (
            transmittance(
                state_new.smoke,
                state_new.agent_pos,
                kappa_B=CEILING_KAPPA,
                k=k,
            )
            < 1.0
        )  # [n_agents, k, k]
        cover = carrier.mean(axis=(-2, -1))  # [n_agents]
        exposed = carrier.any(axis=(-2, -1)) & alive  # smoke in crop at all
        n_exp = jnp.maximum(exposed.sum(dtype=jnp.float32), 1.0)
        ceiling_sum = ceiling_sum + jnp.where(
            fire_active, jnp.where(alive, cover, 0.0).sum() / n_alive, 0.0
        )
        exposed_sum = exposed_sum + jnp.where(
            fire_active, exposed.sum(dtype=jnp.float32) / n_alive, 0.0
        )
        masked_exp_sum = masked_exp_sum + jnp.where(
            fire_active,
            jnp.where(exposed[None, :], per_agent, 0.0).sum(-1) / n_exp,
            0.0,
        )
        exp_agents = exp_agents + jnp.where(
            fire_active, exposed.any().astype(jnp.float32), 0.0
        )
        return (
            obs_new,
            state_new,
            masked_sum,
            fire_steps,
            det_num,
            det_den,
            ceiling_sum,
            exposed_sum,
            masked_exp_sum,
            exp_agents,
        ), None

    n_cand = kappas.shape[0]
    zc, z0 = jnp.zeros((n_cand,), jnp.float32), jnp.float32(0.0)
    init = (obs0, state0, zc, z0, zc, z0, z0, z0, zc, z0)
    (
        _,
        state_f,
        masked_sum,
        fire_steps,
        det_num,
        det_den,
        ceiling_sum,
        exposed_sum,
        masked_exp_sum,
        exp_agents,
    ), _ = jax.lax.scan(body, init, jax.random.split(k_run, cfg.horizon))
    return {
        "masked_sum": masked_sum,
        "fire_steps": fire_steps,
        "det_num": det_num,
        "det_den": det_den,
        "ceiling_sum": ceiling_sum,
        "exposed_sum": exposed_sum,
        "masked_exp_sum": masked_exp_sum,
        "exp_agents": exp_agents,
        "burnt_fraction": (state_f.hazard != FUEL).mean(dtype=jnp.float32),
        "survival_rate": state_f.agent_alive.mean(dtype=jnp.float32),
        "mean_smoke_exposure": state_f.ep_smoke_sum / jnp.float32(cfg.horizon),
    }


def run_severity(
    key: jax.Array,
    cfg: EnvConfig,
    kappas: tuple[float, ...],
    n_eps: int,
    policy=None,
) -> dict:
    """`n_eps` episodes, vmapped; ratio estimators pooled over episodes."""
    kap = jnp.asarray(kappas, jnp.float32)
    run = jax.jit(
        jax.vmap(lambda kk: episode_observables(kk, cfg, kap, policy=policy))
    )
    out = {k: np.asarray(v) for k, v in run(jax.random.split(key, n_eps)).items()}
    # Pool numerators/denominators across episodes: both observables are
    # ratios of step- and cell-counts, so pooling weights each step and
    # each Burning ring cell equally (an episode mean would over-weight
    # episodes with little fire).
    fire_steps = out["fire_steps"].sum()
    det_den = out["det_den"].sum()
    return {
        "n_eps": int(n_eps),
        "fire_active_steps_per_ep": float(out["fire_steps"].mean()),
        "detection_samples": float(det_den),
        "masked_frac": (out["masked_sum"].sum(0) / max(fire_steps, 1.0)).tolist(),
        "detection": (out["det_num"].sum(0) / max(det_den, 1.0)).tolist(),
        # Diagnostics: sup over kappa_B of masked_frac, and the same
        # quantity restricted to agents with any smoke in their crop.
        "masked_frac_ceiling": float(out["ceiling_sum"].sum() / max(fire_steps, 1.0)),
        "exposed_agent_share": float(out["exposed_sum"].sum() / max(fire_steps, 1.0)),
        "masked_frac_exposed": (
            out["masked_exp_sum"].sum(0) / max(out["exp_agents"].sum(), 1.0)
        ).tolist(),
        "burnt_fraction": float(out["burnt_fraction"].mean()),
        "survival_rate": float(out["survival_rate"].mean()),
        "mean_smoke_exposure": float(out["mean_smoke_exposure"].mean()),
    }


def e2c_q(kappas: tuple[float, ...]) -> list[float]:
    """E2C cross-reference q(kappa_B), exact from the shared tau profile.

    q = 1 - prod_t (1 - tau_t) over the pre-commitment steps — the
    zero-MC-error form of the M4.2 prediction (the two agreed there to
    within MC error at every grid point). Geometry-dependent by
    construction: these numbers are Option-A E2C, and must be quoted as
    such (M4.2 ruling item 5).
    """
    out = []
    for kb in kappas:
        taus = np.asarray(tau_profile(e2c_config(float(kb)), 1))
        out.append(float(1.0 - np.prod(1.0 - taus)))
    return out


def in_band(values: list[float], band: tuple[float, float]) -> list[bool]:
    return [bool(band[0] <= v <= band[1]) for v in values]


def band_intersection(rows: dict, kappas: tuple[float, ...]) -> dict:
    """Which candidates satisfy all three bands (M4.3 lock question)."""
    masked_ok = in_band(rows["masked_frac_medium"], BANDS["masked_frac_medium"])
    det_ok = in_band(rows["detection_medium"], BANDS["detection_medium"])
    q_ok = in_band(rows["e2c_q"], BANDS["e2c_q"])
    all_ok = [a and b and c for a, b, c in zip(masked_ok, det_ok, q_ok, strict=True)]
    return {
        "masked_frac_medium_ok": masked_ok,
        "detection_medium_ok": det_ok,
        "e2c_q_ok": q_ok,
        "all_three_ok": all_ok,
        "intersection": [float(k) for k, ok in zip(kappas, all_ok, strict=True) if ok],
    }


def _git_commit() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def _load_probe(spec: str, kappa_B: float):
    """`severity=ckpt_dir` -> (severity, policy_fn, cfg) at the probe's
    own training kappa_B (config-hash guarded by the eval harness)."""
    from che.eval.harness import load_params, make_policy_fn

    severity, ckpt_dir = spec.split("=", 1)
    cfg = load_config(SEVERITY_CONFIGS[severity])
    cfg = dataclasses.replace(
        cfg,
        env=dataclasses.replace(
            cfg.env,
            theta=dataclasses.replace(cfg.env.theta, kappa_B=kappa_B),
        ),
    )
    params, step_n = load_params(ckpt_dir, cfg)
    return severity, make_policy_fn(cfg, params), cfg, step_n


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--n-eps", type=int, default=64)
    p.add_argument(
        "--probe-ckpt",
        action="append",
        default=[],
        metavar="SEVERITY=DIR",
        help="evaluate under a trained probe policy (repeatable)",
    )
    p.add_argument(
        "--probe-kappa-B",
        type=float,
        default=0.0,
        dest="probe_kappa_B",
        help="kappa_B the probe policies were trained at (hash guard)",
    )
    p.add_argument(
        "--kappas",
        type=float,
        nargs="+",
        default=None,
        help="override the candidate grid (e.g. a saturation probe)",
    )
    p.add_argument(
        "--out-dir", type=Path, default=Path("che/bench/results/phase4/m43")
    )
    p.add_argument("--out-name", default="coupling_b_calibration.json")
    args = p.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    key = jax.random.PRNGKey(args.seed)
    t0 = time.perf_counter()

    kappas = tuple(args.kappas) if args.kappas else KAPPA_CANDIDATES
    configs: dict[str, Config] = {
        name: load_config(path) for name, path in SEVERITY_CONFIGS.items()
    }
    k_probe = args.probe_kappa_B

    random_rows, probe_rows = {}, {}
    for si, (name, cfg) in enumerate(configs.items()):
        k_sev = jax.random.fold_in(key, si)  # CRN: same episode keys per severity
        random_rows[name] = run_severity(k_sev, cfg.env, kappas, args.n_eps)
        print(
            f"[random/{name}] masked_frac "
            f"{random_rows[name]['masked_frac'][0]:.3f}..."
            f"{random_rows[name]['masked_frac'][-1]:.3f}  detection "
            f"{random_rows[name]['detection'][0]:.3f}..."
            f"{random_rows[name]['detection'][-1]:.3f}",
            flush=True,
        )

    for spec in args.probe_ckpt:
        name, policy, pcfg, step_n = _load_probe(spec, k_probe)
        si = list(SEVERITY_CONFIGS).index(name)
        row = run_severity(
            jax.random.fold_in(key, si), pcfg.env, kappas, args.n_eps, policy=policy
        )
        row["ckpt"] = spec.split("=", 1)[1]
        row["ckpt_step"] = step_n
        probe_rows[name] = row
        print(
            f"[probe/{name}] step {step_n} masked_frac "
            f"{row['masked_frac'][0]:.3f}...{row['masked_frac'][-1]:.3f} "
            f"(ceiling {row['masked_frac_ceiling']:.3f})",
            flush=True,
        )

    q = e2c_q(kappas)
    bands_source = {
        "masked_frac_medium": (probe_rows or random_rows)["medium"]["masked_frac"],
        "detection_medium": (probe_rows or random_rows)["medium"]["detection"],
        "e2c_q": q,
    }
    payload = {
        "kappa_candidates": list(kappas),
        "bands": BANDS,
        "detection_ring": {
            "distance": DETECTION_DIST,
            "halfwidth": DETECTION_HALFWIDTH,
            # M4.2 Finding-1 obligation: must be 1.0 for the band to mean
            # anything (a single-cell source beyond the quadrature's reach
            # would read tau == 1 and inflate detection to 1).
            "endpoint_sampled_fraction": endpoint_sampled_fraction(
                configs["medium"].env.obs_window
            ),
        },
        "random_policy": random_rows,
        "probe_policy": probe_rows,
        "probe_kappa_B": k_probe,
        "e2c_q": q,
        "e2c_geometry": "Option A (d=2, l_f=2, ell=4, k=9)",
        "band_check": band_intersection(bands_source, kappas),
        "band_check_source": "probe" if probe_rows else "random",
        "n_eps": args.n_eps,
        "jax_version": jax.__version__,
        "backend": jax.default_backend(),
        "git_commit": _git_commit(),
        "seed": args.seed,
        "wall_seconds": time.perf_counter() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    path = args.out_dir / args.out_name
    path.write_text(json.dumps(payload, indent=2) + "\n")

    src = (probe_rows or random_rows)["medium"]
    print(
        f"\n{'kappa_B':>8} {'masked':>8} {'mask|exp':>9} {'detect':>8} "
        f"{'E2C q':>8}   bands"
    )
    for i, kb in enumerate(kappas):
        bc = payload["band_check"]
        flags = "".join(
            "✓" if bc[f][i] else "✗"
            for f in ("masked_frac_medium_ok", "detection_medium_ok", "e2c_q_ok")
        )
        print(
            f"{kb:8.2f} {bands_source['masked_frac_medium'][i]:8.3f} "
            f"{src['masked_frac_exposed'][i]:9.3f} "
            f"{bands_source['detection_medium'][i]:8.3f} {q[i]:8.3f}   {flags}"
        )
    print(
        f"\nMedium masked_frac ceiling (kappa_B -> inf): "
        f"{src['masked_frac_ceiling']:.4f}   "
        f"exposed-agent share: {src['exposed_agent_share']:.3f}   "
        f"fire-active steps/ep: {src['fire_active_steps_per_ep']:.0f}"
    )
    print(f"intersection: {payload['band_check']['intersection']}")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
