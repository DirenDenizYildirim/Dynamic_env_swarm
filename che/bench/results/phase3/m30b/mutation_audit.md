# M3.0b Audit 3 — mutation audit of test power

Procedure: one mutation at a time — apply, run the full CPU suite
(`uv run pytest che/tests`, 81 tests at baseline), record failures,
`git checkout --` the mutated file, next. Baseline suite green before
the first mutation.

**Deviation note:** the milestone routes this audit to the local
`m31-structure` branch; that branch does not exist in this remote
container (see `README.md`, deviation 1). The audit ran against the code
at `8de4976` (M3.0-complete — identical for every mutated file) on the
session branch. The prompt's companion check — "the M3.1 nesting test
(f_weak=0, lambda=0 bitwise-recovers 8de4976) exists and is green" —
could not be performed: no M3.1 code exists here. It must be re-checked
on the real `m31-structure` before merge. Because M3.1's suite is a
superset of M3.0's for the files mutated here, a catch by the M3.0 suite
carries over; the one gap found (mutation g) is closed by a new test in
this milestone's second commit, to be cherry-picked onto
`m31-structure`.

| # | Mutation | Caught? | Failing test(s) |
|---|---|---|---|
| a | Lethality vs pre-step `h` instead of `h'` (call-site: `agent_step` fed `state.hazard`) | **YES** | `test_lethality.py::test_step_ignition_under_stationary_agent_kills_and_penalizes`, `test_lethality.py::test_newly_dead_agent_does_not_collect` |
| b | Burnt cells impassable (`blocked |= hazard' == BURNT`) | **YES** | `test_lethality.py::test_burnt_is_passable_and_harmless` |
| c | Obs planes order swapped (hazard ↔ smoke in the `jnp.stack`) | **YES** | `test_env.py::test_obs_crop_border_correctness` |
| d | Obs crop transposed (`swapaxes(0, 1)` on the k×k window) | **YES** | `test_env.py::test_obs_crop_border_correctness` |
| e | GAE bootstraps through done (drop the `(1-done)` gate) | **YES** (partial run) | `test_ippo.py::test_gae_closed_form` |
| f | Reward reads smoke (`+ 1e-6 * mean(rho)`) | NOT RUN | — |
| g | `kappa_A` branch consumes its PRNG key only when `kappa_A > 0` | NOT RUN | — |

Notes:

- **c/d single-point coverage:** both observation mutations are caught by
  exactly one test, `test_obs_crop_border_correctness`. It is
  well-aimed — its probes are deliberately asymmetric (food at relative
  (0,+1), Burning at (+1,0)), which is precisely what kills both a plane
  swap and a transposition — but it is the *only* line of defense for
  obs semantics. Flagged for awareness, not action: the test would have
  to be weakened (not merely reorganized) for these bugs to slip
  through, and Audit 4's numeric crosscheck (0 mismatches over every
  agent × 3 timesteps × 5 planes, edge padding included) independently
  confirms the current implementation.
- Mutation a is implemented at the `step()` call site (passing
  `state.hazard` in place of `hazard_new`), the minimal edit matching
  the described bug.

## Incomplete rows — honest status (2026-07-20, session paused by human)

- **e:** `test_gae_closed_form` failed against the mutation (recorded in
  two independent runs), so the mutation is caught. What did NOT
  complete is a full-suite pass under (e): the runs stalled at ~86%
  because this remote container suspends background processes when the
  session idles, and the human interrupted the foreground retry. The
  pbt/percolation/reward-independence/scaffold files were never
  finished under (e) — irrelevant to "caught?", relevant only to a
  complete failure inventory.
- **f:** not run. Prediction from reading the suite (not a substitute
  for the run): `test_reward_independence.py` compares rewards with
  exact float equality across a smoke-only difference of Δρ = 3.5, so
  `+ 1e-6·mean(ρ)` shifts reward by ~3.5e-6 ≫ float32 ULP and should
  fail both tests. Run to confirm.
- **g:** not run. Prediction: **the current suite cannot catch it** —
  `k_seed` is a dedicated stream (split per kernel in `env.step`), so
  gating its consumption on `kappa_A > 0` changes no other stream and
  is bitwise invisible behaviorally; `test_nesting` passes either way.
  The planned missing test (verified feasible against 8de4976): a
  structural invariant-#3 test asserting the jaxpr of
  `coupling_a_seed_mask` at `kappa_A = 0.0` still contains the PRNG
  primitives (`random_bits`; a Python-level gate removes them). To be
  added when the audit resumes.
