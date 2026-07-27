"""M4.2 ★ Theorem-1 E2C validation ★ (theory §5 Thm. 1, §10 hook), CPU scale.

Acceptance (phase-4 prompt M4.2, human-ruled 2026-07-27):

1. empirical J* within 2·SE of the *numeric* prediction 1/2 + q/2 at
   every kappa_B grid point;
2. the memorizing (always-L) policy sits at 1/2, flat in kappa_B;
3. J*(0) >= 0.99;
4. J*(kappa_B large) - 1/2 <= 0.02.

Protocol matching (the M3.3 lesson, applied forward): the predicted and
empirical curves share every constant — geometry, (sigma_s, eta), the
smoke-step protocol, k, and the shared `transmittance` — but *not* their
PRNG streams, and not their code path: the prediction draws
Bernoulli(tau) directly from `transmittance`, the empirical curve reads
the fire out of a real `observe()` crop. With shared keys and a shared
path the acceptance test would collapse into the arithmetic identity
J = q + (1 - q)/2 and would prove nothing.

The sweep-dependent tests are @slow (a few minutes on CPU); the
structural and side-channel tests below are cheap and stay in the
default suite.
"""

import jax
import jax.numpy as jnp
import numpy as np
import pytest
from jax.scipy.stats import chi2

from che.env import e2c, observation
from che.env.e2c import (
    D_PATH,
    K_OBS,
    KAPPA_GRID,
    L_F,
    SIDE_L,
    SIDE_R,
    e2c_config,
    run_episodes,
    run_sweep,
    tau_profile,
)

N_EPISODES = 8192  # >= the 4096 phase-prompt floor; SE(J) <= 0.0055
N_MC = 8192

# --- Acceptance-1 statistical gate (human ruling 2026-07-27, final;
# supersedes both the phase prompt's per-point 2·SE spec and the
# joint-chi2-only amendment). Three conditions on the per-point
# z = delta / SE(delta), all required, each catching what the others
# cannot:
#
#   (a) max |z| <= 2.69       Sidak FWER 5% across the grid — catches a
#                             localized gross error at a single kappa_B;
#   (b) sum z^2 vs chi2(n),   catches diffuse magnitude misfit that no
#       p >= 0.05             single point flags (every point at -2 sigma
#                             passes (a), fails (b));
#   (c) |mean z| <= 2/sqrt(n) catches signed systematic drift that passes
#                             both (every point at -1 sigma passes (a)
#                             and (b), fails (c)).
#
# Why not the prompt's per-point 2·SE: applied across the 7 informative
# points it rejects a *correct* implementation ~28% of the time
# (1 - 0.9545^7). The 8-seed replicate diagnostic
# (`phase4/m42/e2c_replicates.json`) measures z ~ N(0, 1) — pooled mean
# +0.025, sd 0.990, 5.4% beyond 2 sigma against 4.6% expected — so the
# gate was the problem, not the implementation. n counts every grid
# point; kappa_B = 0 is deterministic (tau == 1 => q == 1) and
# contributes z = 0 to all three statistics.
ACCEPT_MAX_ABS_Z = 2.69
ACCEPT_CHI2_P = 0.05
ACCEPT_MEAN_ABS_Z = 2.0 / np.sqrt(len(KAPPA_GRID))


@pytest.fixture(scope="module")
def sweep() -> list[dict]:
    return run_sweep(jax.random.PRNGKey(0), n_episodes=N_EPISODES, n_mc=N_MC)


@pytest.mark.slow
def test_empirical_matches_numeric_prediction(sweep):
    """Acceptance 1 — the Theorem-1 handshake, under the final gate."""
    print("\nkappa_B   J*_emp    J*_pred    delta       z      q_mc")
    z = []
    for p in sweep:
        z_p = p["delta"] / p["se_delta"] if p["se_delta"] > 0 else 0.0
        z.append(z_p)
        print(
            f"{p['kappa_B']:6.2f}  {p['j_optimal']:.4f}    "
            f"{p['j_predicted']:.4f}    {p['delta']:+.4f}  {z_p:+6.2f}   "
            f"{p['q_mc']:.4f}"
        )
    z = np.asarray(z)
    max_abs_z = float(np.abs(z).max())
    chi2_stat = float((z**2).sum())
    p_value = float(chi2.sf(chi2_stat, z.size))
    mean_z = float(z.mean())
    print(
        f"(a) max|z| = {max_abs_z:.2f} (gate {ACCEPT_MAX_ABS_Z})\n"
        f"(b) sum z^2 = {chi2_stat:.2f} on {z.size} dof -> p = {p_value:.3f} "
        f"(gate >= {ACCEPT_CHI2_P})\n"
        f"(c) mean z = {mean_z:+.2f} (gate |.| <= {ACCEPT_MEAN_ABS_Z:.2f})"
    )
    assert max_abs_z <= ACCEPT_MAX_ABS_Z, (
        f"(a) localized misfit: max|z| = {max_abs_z:.2f} at "
        f"kappa_B = {sweep[int(np.abs(z).argmax())]['kappa_B']}"
    )
    assert p_value >= ACCEPT_CHI2_P, (
        f"(b) diffuse magnitude misfit: sum z^2 = {chi2_stat:.2f} on "
        f"{z.size} dof, p = {p_value:.4f}"
    )
    assert abs(mean_z) <= ACCEPT_MEAN_ABS_Z, (
        f"(c) signed systematic drift: mean z = {mean_z:+.3f}"
    )


@pytest.mark.slow
def test_memorizing_policy_flat_at_half(sweep):
    """Acceptance 2 — Thm. 1(2): the signal-blind policy is worth 1/2 for
    every kappa_B, so the memorization gap is exactly q/2."""
    for p in sweep:
        assert abs(p["j_memorizing"] - 0.5) <= 2 * p["se_j_memorizing"], (
            f"kappa_B={p['kappa_B']}: memorizing {p['j_memorizing']:.4f}"
        )
    values = [p["j_memorizing"] for p in sweep]
    se = max(p["se_j_memorizing"] for p in sweep)
    assert max(values) - min(values) <= 6 * se  # flat, not trending


@pytest.mark.slow
def test_j_star_at_zero_and_large_kappa(sweep):
    """Acceptance 3 and 4 — the curve spans the whole gap: full
    information at kappa_B = 0, total perceptual denial at the top."""
    lo = min(sweep, key=lambda p: p["kappa_B"])
    hi = max(sweep, key=lambda p: p["kappa_B"])
    assert lo["kappa_B"] == 0.0
    assert lo["j_optimal"] >= 0.99, lo["j_optimal"]
    assert hi["j_optimal"] - 0.5 <= 0.02, (hi["kappa_B"], hi["j_optimal"])


@pytest.mark.slow
def test_q_estimators_agree(sweep):
    """The three routes to q must agree: the prediction MC (Bernoulli on
    `transmittance`), the full `observe()` pipeline, and the closed
    product 1 - prod(1 - tau). The second is the real content of the
    handshake — it checks the *composition* (crop offsets, plane order,
    reveal plumbing) that the prediction path never touches."""
    for p in sweep:
        se = np.hypot(p["se_q_mc"], p["se_q_empirical"])
        assert abs(p["q_mc"] - p["q_empirical"]) <= 3 * se + 1e-12, p
        assert abs(p["q_mc"] - p["q_analytic"]) <= 3 * p["se_q_mc"] + 1e-12, p


@pytest.mark.slow
def test_side_channel_is_quantified(sweep):
    """M4.2 Finding 2 (human ruling item 3): masking is itself
    informative when occlusion co-locates with threat. At kappa_B = 0
    nothing is masked and the plane-7 oracle is at chance; once masking
    is live the oracle identifies Z almost perfectly — which is why the
    scored policies read content planes only."""
    lo = min(sweep, key=lambda p: p["kappa_B"])
    assert abs(lo["oracle_accuracy"] - 0.5) <= 2 * lo["se_oracle_accuracy"]
    for p in sweep:
        if p["kappa_B"] >= 1.0:
            assert p["oracle_accuracy"] >= 0.95, p


def test_geometry_stays_in_the_quadrature_sampled_regime():
    """M4.2 Finding 1 guard (Option A). The phase-prompt rule
    k >= 2(d + l_f) + 1 must hold, and — the constraint that actually
    bit — every pre-commitment step must sit close enough for the
    midpoint quadrature to sample the fire cell, i.e. tau < 1 for
    kappa_B > 0. At the prompt's illustrative d = 6 the first two steps
    give tau == 1 exactly and q == 1 for every kappa_B."""
    assert K_OBS >= 2 * (D_PATH + L_F) + 1
    taus = np.asarray(tau_profile(e2c_config(1.0), SIDE_R))
    assert taus.shape == (D_PATH + 1,)
    assert (taus < 1.0).all(), taus
    # Monotone: closer + denser smoke => less transmitted, step by step.
    assert (np.diff(taus) < 0).all(), taus


def test_corridors_are_exchangeable():
    """Nothing but the fire distinguishes L from R: the tau profile is
    identical for either draw of Z (so the prediction is Z-free), and the
    *mirror* candidate's ray carries no smoke — tau == 1 exactly, which
    is the mechanism behind the plane-7 side channel."""
    cfg = e2c_config(2.0)
    assert (tau_profile(cfg, SIDE_L) == tau_profile(cfg, SIDE_R)).all()
    # Mirror cell: same geometry, no smoke on the ray.
    smoke = jnp.zeros((13, 13), jnp.float32).at[6, 6 + L_F].set(2.5)
    tau = observation.transmittance(
        smoke, jnp.array([[6 - D_PATH, 6]], jnp.int32), kappa_B=2.0, k=K_OBS
    )
    r = K_OBS // 2
    assert tau[0, r + D_PATH, r + L_F] < 1.0  # the smoky (Z) side
    assert tau[0, r + D_PATH, r - L_F] == 1.0  # the clean (mirror) side


def test_scored_policies_never_read_the_visibility_plane(monkeypatch):
    """Ruling item 3: the Thm.-1 policies use the content channel only.
    Destroying plane 7 (forcing "everything was visible") must leave the
    optimal and memorizing outcomes bitwise unchanged while collapsing
    the oracle to chance."""
    cfg = e2c_config(2.0)
    key = jax.random.PRNGKey(11)
    before = run_episodes(key, cfg, 1024)

    def all_visible(state, config, obs_key=None):
        obs = observation.observe(state, config, obs_key)
        return {"grid": obs["grid"].at[..., 7].set(1.0), "vec": obs["vec"]}

    monkeypatch.setattr(e2c, "observe", all_visible)
    after = run_episodes(key, cfg, 1024)

    for channel in ("success_optimal", "success_memorizing", "informed"):
        assert (before[channel] == after[channel]).all(), channel
    assert float(before["oracle_correct"].mean()) > 0.9
    assert abs(float(after["oracle_correct"].mean()) - 0.5) < 0.05


def test_zero_slack_walk():
    """The corridor walk realizes Thm. 1's zero-slack structure: entering
    corridor Z is fatal, the other corridor reaches the goal."""
    cfg = e2c_config(0.0)
    out = run_episodes(jax.random.PRNGKey(3), cfg, 512)
    # kappa_B = 0 => always informed => the optimal policy never dies.
    assert bool(out["informed"].all())
    assert bool(out["success_optimal"].all())
    # Always-L survives exactly when the fire is in the *other* corridor,
    # i.e. when Z = R.
    assert (out["success_memorizing"] == out["z_is_right"]).all()


def test_sweep_grid_spans_the_gap():
    """The grid must include kappa_B = 0 and a large point (prompt M4.2)."""
    assert KAPPA_GRID[0] == 0.0
    assert KAPPA_GRID[-1] >= 5.0
    assert list(KAPPA_GRID) == sorted(KAPPA_GRID)
