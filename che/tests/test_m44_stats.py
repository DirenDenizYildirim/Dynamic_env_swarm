"""Pin the M4.4 seed-level decision rule.

`che.scripts.m44_report.classify` is the boundary the M4.4 inertness
falsifier is evaluated against, so the rule is fixed here rather than
left to whatever the script happens to do. Pure numpy — no JAX, no data
files, runs in milliseconds.
"""

import numpy as np

from che.scripts.m44_report import classify, is_separated, sigma_seed


def test_overlapping_ranges_and_small_delta_are_within_noise():
    a = np.array([0.70, 0.74])
    b = np.array([0.71, 0.75])
    _, _, overlap, verdict = classify(a, b)
    assert overlap
    assert verdict == "within-noise"
    assert not is_separated(verdict)


def test_strong_requires_both_clauses():
    """The M4.4 High-survival shape: disjoint ranges AND |delta| > 2 sigma."""
    a = np.array([0.9408, 0.9225])
    b = np.array([0.8721, 0.8159])
    delta, sig, overlap, verdict = classify(a, b)
    assert not overlap
    assert abs(delta) > 2 * sig
    assert verdict == "SEPARATED(strong)"


def test_disjoint_but_within_two_sigma_is_only_weak():
    """Disjointness alone has p = 1/3 under the null at 2v2, so it must
    not earn the strong grade on its own."""
    a = np.array([0.10, 0.30])
    b = np.array([0.31, 0.51])
    delta, sig, overlap, verdict = classify(a, b)
    assert not overlap
    assert abs(delta) <= 2 * sig
    assert verdict == "SEPARATED(weak)"


def test_at_two_seeds_overlap_always_implies_within_noise():
    """At 2 seeds per arm the |delta| > 2 sigma clause can never fire on
    its own, so "weak" always means "disjoint ranges, small delta".

    Proof: writing r for an arm's range, sigma_seed = sqrt(r_a^2+r_b^2)/2,
    while overlapping intervals force |delta| <= (r_a+r_b)/2, and
    (r_a+r_b)^2 <= 2(r_a^2+r_b^2) <= 4(r_a^2+r_b^2). So overlap implies
    |delta| <= 2 sigma_seed. Checked here on random arms so the property
    is pinned rather than merely argued.
    """
    rng = np.random.default_rng(0)
    seen_overlap = 0
    for _ in range(2000):
        a = rng.normal(0.0, 1.0, 2)
        b = rng.normal(0.3, 1.0, 2)
        delta, sig, overlap, verdict = classify(a, b)
        if overlap:
            seen_overlap += 1
            assert abs(delta) <= 2 * sig + 1e-12
            assert verdict == "within-noise"
    assert seen_overlap > 100  # the branch was actually exercised


def test_sigma_seed_pools_both_arms_and_is_symmetric():
    a = np.array([0.1, 0.3])
    b = np.array([0.5, 0.5])
    assert sigma_seed(a, b) == sigma_seed(b, a)
    # sqrt(mean([var(a, ddof=1), 0])) = sqrt(0.02 / 2)
    assert sigma_seed(a, b) == np.sqrt(np.var(a, ddof=1) / 2)


def test_delta_sign_is_kappa_arm_minus_control():
    a = np.array([0.50, 0.50])
    b = np.array([0.40, 0.40])
    delta, _, _, _ = classify(a, b)
    assert delta < 0


def test_three_seed_arm_is_accepted():
    """Medium carries three seeds (amendment 4); the rule must not
    assume equal or two-element arms."""
    a = np.array([0.7443, 0.7365, 0.7253])
    b = np.array([0.7596, 0.7406, 0.7622])
    delta, sig, overlap, verdict = classify(a, b)
    assert overlap and verdict == "within-noise"
    assert delta > 0 and sig > 0
