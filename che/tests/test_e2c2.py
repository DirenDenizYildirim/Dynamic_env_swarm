"""M5.2 ★ Remark-2 VoC validation ★ (theory §5 Remark 2′/2″/2‴), CPU scale.

Acceptance (phase-5 prompt M5.2, as amended by the pre-flight rulings of
2026-07-28):

1. the M4.2 three-condition gate (Sidak 2.69 / joint chi2 p >= 0.05 /
   |mean z| <= 2/sqrt(n)) applied to the **denied pinned** curve against
   its numeric prediction 1/2 + q/2 — the protocol-matched arm, which is
   the only one that is exactly predictable and therefore the only one
   that can be gated (round-2 ruling item 1);
2. the free-comms curve >= 0.99 at every kappa_B;
3. measured VoC monotonically increasing across the grid (isotonic
   within noise).

The dawdle family is *measured and reported*, never gated: it is the
answer to Remark 2″'s residual, and Remark 2‴ explicitly deferred its
constants to this milestone rather than letting a chat heuristic into the
theory doc.

Protocol matching carries over from M4.2 unchanged: predicted and
empirical curves share every constant but neither their PRNG streams nor
their code path, or the gate would collapse to the identity
J = q + (1 - q)/2.

The sweep-dependent tests are @slow; the structural ones below are cheap
and stay in the default suite.
"""

import dataclasses

import jax
import jax.numpy as jnp
import numpy as np
import pytest
from jax.scipy.stats import chi2

from che.env import e2c2
from che.env.e2c2 import (
    IDLE_SCHEDULES,
    KAPPA_GRID,
    PINNED_SCHEDULE,
    SIDE_R,
    e2c2_config,
    run_episodes,
    run_sweep,
    tau_profile,
)

N_EPISODES = 4096  # the phase-prompt floor; SE(J) <= 0.0078
N_MC = 8192

# Same three-condition gate as M4.2, and for the same reason — the
# per-point 2·SE spec rejects a correct implementation ~28 % of the time
# across the grid. See test_e2c.py for the full derivation; the constants
# are restated rather than imported so a change there cannot silently
# retune this gate.
ACCEPT_MAX_ABS_Z = 2.69
ACCEPT_CHI2_P = 0.05
ACCEPT_MEAN_ABS_Z = 2.0 / np.sqrt(len(KAPPA_GRID))


@pytest.fixture(scope="module")
def sweep() -> list[dict]:
    return run_sweep(jax.random.PRNGKey(0), n_episodes=N_EPISODES, n_mc=N_MC)


# --- Acceptance 1: the gated arm ---------------------------------------


@pytest.mark.slow
def test_pinned_arm_matches_numeric_prediction(sweep):
    """J_pinned = 1/2 + q/2, on M4.2's commit schedule and M4.2's q."""
    z = np.array(
        [p["delta_gate"] / p["se_delta_gate"] if p["se_delta_gate"] > 0 else 0.0
         for p in sweep]
    )
    chi2_stat = float((z**2).sum())
    p_value = float(chi2.sf(chi2_stat, z.size))
    rows = "\n".join(
        f"  kappa_B={p['kappa_B']:>4.1f}  J={p['j_pinned']:.4f}  "
        f"pred={p['j_predicted']:.4f}  z={zi:+.2f}"
        for p, zi in zip(sweep, z, strict=True)
    )
    assert np.abs(z).max() <= ACCEPT_MAX_ABS_Z, (
        f"(a) localized misfit: max |z| = {np.abs(z).max():.2f}\n{rows}"
    )
    assert p_value >= ACCEPT_CHI2_P, (
        f"(b) diffuse magnitude misfit: sum z^2 = {chi2_stat:.2f} on "
        f"{z.size} dof -> p = {p_value:.3f}\n{rows}"
    )
    assert abs(z.mean()) <= ACCEPT_MEAN_ABS_Z, (
        f"(c) systematic drift: mean z = {z.mean():+.3f}\n{rows}"
    )


# --- Acceptance 2: the free arm ----------------------------------------


@pytest.mark.slow
def test_free_arm_is_at_one_everywhere(sweep):
    """Messages are not attenuated by smoke (Def. 7: T_K does not read h),
    so the courier's success must not decay with kappa_B at all.

    This is the load-bearing half of Remark 2: if the free arm sagged at
    high kappa_B, the "VoC" gap would be partly a perception artifact.
    """
    for p in sweep:
        assert p["j_free"] >= 0.99, (
            f"free arm sags at kappa_B={p['kappa_B']}: {p['j_free']:.4f}"
        )


# --- Acceptance 3: VoC increasing --------------------------------------


@pytest.mark.slow
def test_voc_increases_with_perception_decay(sweep):
    """Remark 2's claim, as a curve: comms is load-bearing exactly when
    perception fails.

    Isotonic within noise — a strictly increasing test would fail on MC
    jitter at the flat high-kappa_B end, where VoC has saturated at 1/2.
    """
    kb = np.array([p["kappa_B"] for p in sweep])
    voc = np.array([p["voc_measured"] for p in sweep])
    se = np.array([np.hypot(p["se_j_free"], p["se_j_pinned"]) for p in sweep])
    assert voc[0] < 0.02, f"VoC must vanish at kappa_B=0, got {voc[0]:.4f}"
    assert voc[-1] > 0.45, f"VoC must saturate near 1/2, got {voc[-1]:.4f}"
    drops = [
        f"kappa_B {kb[i - 1]}->{kb[i]}: {voc[i - 1]:.4f}->{voc[i]:.4f}"
        for i in range(1, len(voc))
        if voc[i] < voc[i - 1] - 2.0 * np.hypot(se[i], se[i - 1])
    ]
    assert not drops, "VoC decreases beyond noise at:\n  " + "\n  ".join(drops)


@pytest.mark.slow
def test_both_voc_definitions_are_reported_and_ordered(sweep):
    """VoC_true <= VoC_gated pointwise (Remark 2″), both increasing.

    The dawdle correction is measured, not gated — but its *sign* is a
    theory claim and is checked: idling can only add observations, so
    q~ >= q and the true VoC can only be smaller.
    """
    for p in sweep:
        assert p["q_tilde"] >= p["q_mc"] - 3.0 * p["se_q_mc"], (
            f"q~ < q at kappa_B={p['kappa_B']}: "
            f"{p['q_tilde']:.4f} < {p['q_mc']:.4f}"
        )
        assert p["voc_true"] <= p["voc_gated"] + 3.0 * p["se_q_mc"]


@pytest.mark.slow
def test_q_estimators_agree(sweep):
    """The three q's — analytic, MC, and through the full observe()
    pipeline — must agree, or the composition is wrong somewhere."""
    for p in sweep:
        assert abs(p["q_mc"] - p["q_analytic"]) <= 4.0 * p["se_q_mc"] + 1e-9, p
        tol = 4.0 * np.hypot(p["se_q_empirical"], p["se_q_mc"]) + 1e-9
        assert abs(p["q_empirical"] - p["q_mc"]) <= tol, p


# --- Structural tests (default suite) ----------------------------------


def test_horizon_is_derived_not_asserted():
    """T = d + l_f + ell, computed from the lethality geometry."""
    assert e2c2.E2C2_HORIZON == e2c2.horizon()
    assert e2c2.horizon() == e2c2.scout_verdict_step() + e2c2.CORRIDOR_LEN
    assert e2c2.scout_verdict_step() == e2c2.D_PATH + e2c2.L_F
    # Remark 2's original T = d + ell + 1 is the l_f = 1 case.
    assert e2c2.L_F != 1 or e2c2.horizon() == e2c2.D_PATH + e2c2.CORRIDOR_LEN + 1


def test_idle_family_is_the_complete_open_loop_family():
    """The optimality argument needs *every* open-loop idle placement, or
    the reported maximum is a lower bound wearing an optimum's label."""
    from math import comb

    assert len(IDLE_SCHEDULES) == comb(e2c2.D_PATH + e2c2.L_F, e2c2.L_F)
    assert len(set(IDLE_SCHEDULES)) == len(IDLE_SCHEDULES)
    for s in IDLE_SCHEDULES:
        assert len(s) == e2c2.D_PATH + e2c2.L_F + 1
        assert s[0] == e2c2.D_PATH and s[-1] == 0
        steps = np.diff(s)
        assert set(np.unique(steps)) <= {-1, 0}, f"non-monotone schedule {s}"
        assert (steps == -1).sum() == e2c2.D_PATH
    # Pinned commits at d and spends none of the slack, so it is shorter
    # than every family member; the member that extends it by idling at
    # the branch is the one that dominates it (see the dawdle test).
    assert PINNED_SCHEDULE == tuple(range(e2c2.D_PATH, -1, -1))
    assert len(PINNED_SCHEDULE) == e2c2.D_PATH + 1
    assert PINNED_SCHEDULE + (0,) * e2c2.L_F in IDLE_SCHEDULES


def test_free_arm_collapses_onto_pinned_under_denial():
    """delta = 1 must delete the comms channel exactly, not approximately.

    Same episode key at both delta ends, so the arms differ only through
    the link draw. Under total denial the courier has nothing but its own
    perception and must reproduce the pinned policy *episode by episode* —
    not merely in the mean.
    """
    for kb in (0.0, 1.0, 8.0):
        k = jax.random.PRNGKey(7)
        denied = run_episodes(k, e2c2_config(kb, 1.0), 256, PINNED_SCHEDULE)
        assert not bool(denied["delivered"].any()), "delta=1 delivered a message"
        assert (denied["success_free"] == denied["success_pinned"]).all(), kb


def test_free_arm_reads_silence_correctly():
    """The scout's death is informative only because delta = 0 makes
    silence unambiguous. Delivered <=> the probed corridor was safe."""
    out = run_episodes(
        jax.random.PRNGKey(11), e2c2_config(2.0, 0.0), 512, PINNED_SCHEDULE
    )
    # The scout probes L, so it survives to report exactly when Z = R.
    assert (out["delivered"] == out["z_is_right"]).all()
    assert bool(out["success_free"].all())


def test_coverage_arm_needs_no_messages():
    """Remark 2′(i): interchangeable expendable agents, at least as many
    as hypotheses, achieve J = 1 under total denial — so VoC is zero there
    and the courier variant's irreplaceable role is what creates it."""
    for kb in (0.0, 2.0, 8.0):
        out = run_episodes(
            jax.random.PRNGKey(5), e2c2_config(kb, 1.0), 256, PINNED_SCHEDULE
        )
        assert bool(out["success_coverage"].all()), kb


def test_courier_never_reads_the_agent_plane(monkeypatch):
    """Q6 blinding ruling: the courier learns the scout's fate *only*
    through messages.

    Poison plane 6 (alive occupancy) with noise. If any scored policy read
    it, the denied arms would move; they must be bit-identical.
    """
    cfg = e2c2_config(1.5, 1.0)
    real_observe = e2c2.observe

    def poisoned(state, config, key=None):
        obs = real_observe(state, config, key)
        noise = jax.random.bernoulli(
            jax.random.PRNGKey(99), 0.5, obs["grid"][..., 6].shape
        ).astype(obs["grid"].dtype)
        return {**obs, "grid": obs["grid"].at[..., 6].set(noise)}

    before = run_episodes(jax.random.PRNGKey(1), cfg, 256, PINNED_SCHEDULE)
    monkeypatch.setattr(e2c2, "observe", poisoned)
    after = run_episodes(jax.random.PRNGKey(1), cfg, 256, PINNED_SCHEDULE)
    for arm in ("success_pinned", "success_dawdle", "informed_pinned"):
        assert (before[arm] == after[arm]).all(), arm


def test_scored_policies_never_read_the_visibility_plane(monkeypatch):
    """M4.2 Finding 2 carries over: plane 7 identifies Z on its own, and
    the scored arms must not touch it."""
    cfg = e2c2_config(1.5, 1.0)
    real_observe = e2c2.observe

    def poisoned(state, config, key=None):
        obs = real_observe(state, config, key)
        return {**obs, "grid": obs["grid"].at[..., 7].set(1.0)}

    before = run_episodes(jax.random.PRNGKey(2), cfg, 256, PINNED_SCHEDULE)
    monkeypatch.setattr(e2c2, "observe", poisoned)
    after = run_episodes(jax.random.PRNGKey(2), cfg, 256, PINNED_SCHEDULE)
    assert (before["success_pinned"] == after["success_pinned"]).all()


def test_dawdling_helps_only_because_the_family_contains_move_first():
    """q~ >= q — but the claim is about the family's *maximum*, and the
    distinction is not pedantic.

    Idling is not free: the smoke field grows every step, so spending a
    slack step early pushes every later observation to a smokier time.
    Schedule (2,2,1,0,0) is measurably *worse* than pinned at kappa_B = 5
    for exactly that reason. What rescues Remark 2″ is that the family
    contains DOMINATING = move immediately, then idle at the branch, whose
    draws are a strict superset of the pinned schedule's — same distances
    at the same times, plus l_f extra draws at the closest cell. So
    q~ >= q with equality iff l_f = 0, as the remark says, and the
    open-loop maximum is what makes it an equality rather than a bound.
    """
    dominating = PINNED_SCHEDULE + (0,) * e2c2.L_F
    assert dominating in IDLE_SCHEDULES

    worse_exists = False
    for kb in (0.5, 1.0, 2.0, 5.0):
        cfg = e2c2_config(kb, 1.0)

        def q_of(sched, cfg=cfg):
            t = np.asarray(tau_profile(cfg, SIDE_R, sched), np.float64)
            return 1.0 - np.prod(1.0 - t)

        q = q_of(PINNED_SCHEDULE)
        assert q_of(dominating) >= q - 1e-12, f"kappa_B={kb}: dominance broken"
        assert max(q_of(s) for s in IDLE_SCHEDULES) >= q - 1e-12, kb
        worse_exists |= any(q_of(s) < q - 1e-9 for s in IDLE_SCHEDULES)
    assert worse_exists, (
        "no idle placement was worse than pinned anywhere on the grid — "
        "then idling would be unconditionally free and this test is no "
        "longer describing the environment"
    )


def test_shares_the_theorem1_geometry():
    """E2C-2 must not drift from E2C: a divergence between the Theorem-1
    and Remark-2 figures has to be about comms, not about the arena."""
    from che.env import e2c

    for name in ("D_PATH", "L_F", "CORRIDOR_LEN", "K_OBS", "GRID", "B_ROW",
                 "B_COL", "SIGMA_S", "ETA"):
        assert getattr(e2c2, name) == getattr(e2c, name), name
    assert e2c2.KAPPA_GRID == e2c.KAPPA_GRID


def test_comms_goes_through_the_production_kernel():
    """Delivery must use Def. 7, not a bespoke coin — otherwise M5.2 would
    validate comms theory against comms code that production never runs."""
    cfg = e2c2_config(1.0, 0.0)
    key = jax.random.PRNGKey(0)
    # A scout that is alive and in range delivers at delta = 0.
    assert bool(e2c2._message_delivered(key, jnp.int32(SIDE_R), cfg))
    # ... and never when the range test fails, which is the kernel's job.
    far = dataclasses.replace(
        cfg, theta=dataclasses.replace(cfg.theta, r_comm=0.0)
    )
    assert not bool(e2c2._message_delivered(key, jnp.int32(SIDE_R), far))
