# Integrity audit — 2026-07-28, pre-M5.0

Read-only audit of `main` @ `0c612b6e8e19c1372592375f097af9a01197cf62`,
run in one session before M5.0 begins. Nothing in `che/`, `CLAUDE.md` or
`docs/decision_log.md` was modified; every proposed correction is a diff for
human review inside the two output documents.

## Outputs

| document | what it is |
|---|---|
| [`citation_audit_2026-07-28.md`](citation_audit_2026-07-28.md) | **Part 1 — citation audit (phantom-rule class).** Every reference to a rule, decision, lock, amendment, precedent, artifact, commit or measured number in `decision_log.md`, `CLAUDE.md` and all phase reports, resolved against written text in the repo. |
| [`../claim_ledger.md`](../claim_ledger.md) | **Part 2 — claim ledger (Remark-2 class).** Every numbered claim in `theory_foundations.md` classified (a) test-validated / (b) scheduled / (c) cited / (d) untested, with the hook or hedge each (d) needs. Doubles as a **paper appendix asset**. |

## Why now

The transcription meta-rule landed at the audited commit: *"a chat ruling binds
only once transcribed into `decision_log.md` or `CLAUDE.md` in the same
session."* It was written after "tooling rule 3c/3d" turned out to be a
phantom. This audit applies that rule **backwards** over the whole repo, to
find the rest of the stock — and applies the Remark-2 lesson (an overclaim by
the author, caught only on a careful re-read) to every other formal claim.

## Headline findings

**Citation audit — 3 dangling, 2 untracked, 3 stale, 1 untraceable, 1 ambiguous.
Clean: 17/17 commit hashes, 35/35 `invariant #N`, 5/5 bibliography entries both
ways, 4/4 precedent citations, 85 path citations.**

1. **C-3 — "D6-proposal" does not exist.** Cited three times, twice as a hard
   PHASE 6 ENTRY GATE. No D6 of any kind is in the repo.
2. **C-4 — "the locked hypothesis" has no written source.** The paper's
   load-bearing claim (Γ > 0, *primary metric task completion rate*), the
   "locked ablation list", the "five locked Phase 7 configs" and "Reading 1,
   locked" are all cited by `theory_foundations.md` and exist nowhere.
   Sharp end: M4.4 showed Coupling B moves **survival**, not completion.
3. **C-9 — the locked β̂_c = 0.500's pivot estimator is not reproducible.**
   `severity_lock.md`'s "R_L logistic centers 0.4985 / 0.5006 / 0.4999" and the
   self-duality row appear in no committed artifact, and
   `che/calibration/estimates.py` never fits a logistic to R_L. The committed
   consensus is 0.4991 and the committed crossings mean 0.5045. The lock is
   defensible; the pivot is currently unauditable.
4. **C-1 / C-2 — `phase4_prompt.md` and `phase5_prompt.md` are untracked.**
   The κ_B lock bands cite a file that is not under version control.
5. **C-5 — "Render audit (standing rule)" names a rule that was never
   written.** The practice is real and worth keeping; only the citation is
   phantom.

**Claim ledger — 57 claims: 32 (a), 12 (b), 5 (c)+4 missing refs, 13 (d), of
which 8 need a mandatory hedge or correction.**

1. **A-1 — Def. 4's Medium prediction was tested and did not survive**, and the
   theory doc does not say so. `def4_variance.md` (registered in advance):
   survival variance **REFUTED** (monotone in severity, High highest);
   completion **NOT CONFIRMED**; environment-level mechanism **CONFIRMED**.
   Remark 2 got a superseded banner the same day it was found wrong — Def. 4
   has had none since 2026-07-20.
2. **A-2 — "the ported PyTorchFire/JaxWildfire kernel" is a false provenance
   claim.** The kernel was implemented from Def. 3
   (`phase0_substrate_prompt.md:41`); neither project appears in the repo,
   dependencies, or bibliography. The wording has already spread into
   `test_percolation.py` and `phase1_2_prompt.md`.
3. **A-3 — Definition 1 omits ρ (smoke) from the state space and the kernel
   product**, contradicting locked **D3**, CLAUDE.md invariant #2, and
   `EnvState`. Prop. 1 is a Markov-closure argument about that factorization,
   so its hypothesis is incomplete as written.
4. **A-4 — the 43/18 divergence rate is not a property of this kernel.**
   `severity_lock.md` already says the asymptotic exponent is unreachable at
   L = 64 (measured effective ≈ 1.6), and Prop. 3's sweep runs at a single β.
   The paper must not quote 43/18 as measured here.

Full severity-ordered action registers are at the end of each document.

## The good news, recorded

Both test suites were re-run against the pinned commit: **123 fast + 12 slow
theory tests PASS**, and the two headline theory results **reproduce their
committed report numbers exactly** — M4.2's eight-row E2C table digit for digit
(max\|z\| 2.11, Σz² 6.55/8 dof, p 0.586, mean z −0.44) and M3.3 v2's
slope 41.18 / matched_ref 41.49 / ratio 0.992 / R² 0.9995. Months later, on a
different machine, without a GPU. That is the M3.3 pinned-key discipline
working as designed, and it means every **(a)** in the ledger is a *verified*
(a) rather than a cited one.

Also clean: all 17 commit hashes, all 35 `invariant #N` references, the
bibliography in both directions, all four "precedent" citations, and the
three-part Q4 fix from the same-day ruling (artifact-persistence rule,
`run_m44_grid.sh` retro-flag, transcription meta-rule) — **3/3 executed**.

## Coverage limits

Chat-transcript claims cannot be checked from here — C-3, C-4 and C-5 may each
have a genuine chat origin, and the meta-rule's own remedy (transcribe or
strike) is the human's call. No GPU run was re-executed; `.npz` contents were
spot-checked only where a JSON sibling existed. See §H of the citation audit.

## Merge sequencing

Per the audit brief: **merge after human review, sequenced after M5.0's next
commit lands.** Nothing here blocks M5.0.
