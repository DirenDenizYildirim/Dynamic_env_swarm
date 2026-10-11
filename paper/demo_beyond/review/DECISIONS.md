# Fix-round decisions (orchestrator, 2026-10-11)

Binding on all four writers in the fix round, so that cross-section fixes
land the same way in every file. Builder decisions for the demonstration
only; the owner may overrule any of them. Nothing here edits
`paper/finale.md`, `CLAUDE.md`, the theory doc or the canonical ledger.

1. **Which reviewer wins.** On a claim's level (overreach, undersell,
   conflict, missing) the keeper's `claims.md` adjudication wins. On a value,
   tag, scope or arithmetic, `numbers.md` wins. On kit syntax, listings,
   theory fidelity and cross-references, `mechanics.md` wins. Where two
   reviews disagree outside those lanes, follow the record they cite and
   say which you followed in your resolutions file.
2. **What to fix.** Every MUST and SHOULD on your files. A NOTE when it is
   clearly correct and cheap, including the length cuts `claims.md` names.
   Skip anything else with a one-line reason.
3. **Prop. 1 finiteness.** §3's argument stands: the smoke field is
   real-valued, so the state space is not finite, and what the proof uses is
   that the set of states reachable within the horizon is finite (finite-
   support kernels; smoke deterministic from zero). App. A (W4) adopts §3's
   argument and says in one sentence that it departs from the theory doc's
   wording, which still calls S and Ω finite. §1 (W1) does not call CHE a
   "finite Dec-POMDP" without that qualification. The owner rules on the
   theory doc (claims.md OWNER ITEMS O-2).
4. **"Predicted before measurement" (CA-4).** Use the keeper's wording
   direction (claims.md C-1): the ordering was recorded at the Coupling-A lock
   from the random-policy calibration, before any trained policy. §1 and §5
   must agree. The owner's abstract is not edited (OWNER ITEMS O-1).
5. **Erdem & Üre: "every adversarially trained arm".** Keep the qualifier
   (the keeper's full-read adjudication: the Non-Robust baseline is
   unattacked). This resolves mechanics M-15. Owner item O-3 records that
   the owner's §2 wording is inaccurate.
6. **Notation.** Keep γ_p and γ_n, the registered names of the secondary
   slopes. The discount factor stays γ and appears only where it is needed
   (Def. 8 / Prop. 4, App. A). §3's notation paragraph (W2) states that the
   subscripted γ_p, γ_n are the secondary design's slopes (§9). The Šidák
   family size keeps m and the critical value is written z_α everywhere
   (§8.2 changes from z_α′). Any other m or n gets a different letter
   inside its own section.
7. **Subscripts in prose.** Bare underscores (κ_A, d_p, A_c, Gamma_H) become
   inline math (`$\kappa_A$`) or Unicode subscripts. Never inside raw HTML,
   which takes Unicode only.
8. **Figure references.** Each figure is named in the prose at or before
   its placement. J1 and J2 are both named in App. J.
9. **Untagged record numbers** get their tag. A number with no row gets a
   VERIFIED row first, or is cut. (Corrected after the re-check, C-R5: the
   first wording, "cut rather than given one now", conflicted with the ledger
   rule that a new number gets its row first. The seven rows the writers
   added in the fix round were re-verified by the numbers auditor.)
10. **Record each finding's outcome** in `paper/demo_beyond/review/resolutions_W<n>.md`:
    `id | action (fixed / skipped) | where / why`, one row per finding on your
    files.
