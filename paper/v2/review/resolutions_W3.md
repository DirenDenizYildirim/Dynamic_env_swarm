# Resolutions: W3 (§3, §4, `alt/04_severity.no_item4.md`), step 4, pass 3

Writer W3, 2026-10-12. These rows cover every finding in RC1, RC2, RN1, RN2 and RM that touches
W3's files, either as the finding's location or as cited evidence. Line numbers are those of
`paper/v2/snapshots/draft1/`. Each changed sentence's provenance row names its finding
(`provenance/03_environment.md`, `04_severity.md`, `04_severity.no_item4.md`). One new row:
V3-1, in `ledger_proposals/W3.md`. RN2 has no finding in W3's files.

| finding ID | outcome (fixed / declined / owner) | what changed, or why not |
|---|---|---|
| RN1-1 (MUST) | fixed | §3.3: "in every configuration reported here" → "in every configuration reported here except the $d_p$ ablation below (the code's default is 0)". The ablation's d_p = 0 runs are ENV-2 (`phase2_report.md:29`) |
| RN1-9 (MUST) | fixed | New VERIFIED row V3-1 (`che/env/env.py:241-243`, read this session; the file matches HEAD). §3.2's "one Burning cell" now carries the tag `N:V3-1` |
| RM-1 (MUST) | fixed | Definition 2's display is now two `aligned` lines, broken after the $R_{\mathrm{task}}$ term, as Definition 1's kernel display is. No symbol changed |
| RM-3 (MUST), the §3.4 table | fixed (the text half) | The header "asserted by" becomes "test (`che/tests/`)", and the cells give `test_nesting.py` and `test_comms.py` only. "(Definition 5, §5)" and the others become "(§5)", "(§6)", "(§7)", and "the observation before masking" becomes "the pre-masking observation". B2's print CSS does the rest (orchestrator decision 3). §4's levels table is not in RM-3's clipped list; it is unchanged |
| RM-9 (OWNER) | owner | Not changed, as directed. Recorded in `provenance/03_environment.md`, Open items, pass 3: Definition 1 omits the weak mask w and the message argument of the observation kernel; TF Def. 1 has the same gap |
| RM-13 | fixed | §4.1, and the same sentence in the alternate: "(§3.2)" → "(§5.1)" for Coupling A |
| RM-16 | fixed | §3.5: "row and column over $L$" → "row and column divided by the grid side", because L is defined only in Definition 4 |
| RM-17 | declined (no change in W3's files) | The T and t clash is fixed where the second meaning is introduced (§9, §10, App. G; W6 and W5). Definition 1 keeps T as the horizon and t as the step, as TF has them; §3.5 already names the budget T\* in updates. The reviewer classes it C (new) |
| RM-18 | declined (no change in W3's files) | The k clash is fixed in §8.2 (W5), as RM proposes; Definition 1's k is TF's link graph |
| RM-20 | owner | Class C (new) and structural. Definition numbers follow TF and are cited across sections (§1 and the abstract cite Definition 2), so moving Definition 2 before §3.2 changes §3's order and other writers' "§3.3" pointers. Recorded for the owner |
| RM-25 | declined (no change in W3's files) | B2's print CSS. Listing 1 must stay byte-identical, so there is no text fix |
| RN1-15 | fixed | §4's opening (and the alternate): "the three levels" → "the three levels", with "three" now tagged `N:CAL-3`, consistent with §1:25. RN1's other locations are §6 (W4) |
| RN1-16 (OWNER) | owner | Numerals describing cited works in §3 and §4 ("two or more agents" in Remark 1, "Corollary 5.4", citation years) stay untagged pending the owner's rule; recorded in both provenance files |
| RC1-27 | fixed | §3.3: "every difference far from all agents" → "fire and structure differ only far from every agent, which pins the alive transition equal"; the test lets smoke differ everywhere (`test_reward_independence.py:8-13`). No new number: the six-cell distance is not stated |
| RC1-28 | fixed | §4.2, first prose use: "the observable band it was locked to, that is, fixed on 2026-07-19, before the main experiment (§4.3)", with the date tagged `N:DX-401`; the grid began on 2026-09-09 (DES-12) |
| RC1-29 | fixed in part; one part declined | Cut "The penalty prices an outcome, not the hazard." The announced "Two tests check clause (i)." becomes "One test of clause (i) asserts …". The unclear IPPO clause becomes "whose update takes each agent's transitions as separate samples under the team reward". **Declined:** "survival is learned through two hazard-blind routes", because it is the DEF. 2 WORDING RULING's own clause (log:5287) and "the first route" refers back to it |
| RC1-30 | fixed | §4.3: "All of them bracket Kesten's ½." → "Their range brackets Kesten's ½." §4.3: "so it can be outrun, barely" → "escape is possible in principle", the lock record's words (`severity_lock.md:36-37`) |
| RC1-38 | fixed | §3: two ", so" clauses became a colon (Listing 2) and a semicolon (message head). §4: the "so it can be outrun" clause is gone (RC1-30). The remaining "so" clauses in §3 and §4 state an inference given in the same sentence (for example, a cell igniting under a standing agent kills it, because the fire kill uses h′) |
| RC1-11 | declined (no change in W3's files) | The fix belongs in W1's reading note under the hero. My status tags ("schematic, no data"; "calibration, no agents") are accurate and are cited only as evidence |
| RC1-39, RC2-4, RM-12 | declined (no change needed in W3's files) | These concern W6's App. A line "Corollary 1(3)". §4.1 states items 1 and 2 only and mentions no dropped item, so App. A's fix stands on its own |
