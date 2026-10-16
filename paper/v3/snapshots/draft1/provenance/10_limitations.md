# Provenance: sections/10_limitations.md

Writer: W5 (Paper v3, step 4.1, 2026-10-14). Checked with
`paper/v3/src/provenance_check.py --strict`. `log` = `docs/decision_log.md`.
v2 material: `paper/v2/sections/10_limitations.md` (items 1–10 at :23-32, the
two later lists at :36-47). v3 keeps only what §1's up-front limitations do
not carry (STUB-SPEC; V3-F6), and points to every caveat that has another home
(`checks/caveats.yaml`).

| # | sentence (verbatim) | support | change from v2, and why |
|---|---|---|---|
| 1 | 7 Limitations and scope | framing | edited (v2 "10 Limitations"; heading as the stub fixes it) |
| 2 | The largest limitations sit where they arise, and §1 lists them first: how much composition the test configuration offered, and what the post hoc interaction check measured there (§6.1, §6.4); the coarse and unevenly applied inert label for communication denial (§4.4); the communication setting that differs between training and test for two arms (§6.2); and one learner, one map and one team size (§1). | framing; paper_v3_prompt.md:217-222 (V3-F6: limitations in front; sited where composition is weak, the interaction check measures it; the inert label coarse and asymmetric; one algorithm, one map size, 12 agents); X4-2 (the train/test setting for ISO and ISO‑4); ENV-6; ENV-11 | new. A pointer sentence (the orchestrator asked that §7 make the central limitations up front; the one-home map, C01, C03, C04, C05, keeps their statements in §6.1, §4.4, §6.2 and §1, so this sentence names them and points, using none of their detection phrases). Replaces v2 10:23 (item 1 in full) and v2 10:27 (item 5). "how much composition ... offered" is written so it reads correctly whatever the check finds |
| 3 | Every comparison in the worked example is at matched compute, 1000 updates per run, and says nothing about other budgets (§6.2). | DES-13 (T\* = 1000; matched budget for every arm); DX-3 | edited from v2 10:44 ("so Γ is a claim at matched compute only"); C11's short form, used once, as allowed here; never "convergence" (`checks/terms.txt`) |
| 4 | No theorem in this paper says that joint training should win; the hypothesis the worked example tests is empirical. | docs/theory_foundations.md:686-689 ("No theorem that joint training wins ... The hypothesis is empirical by design") | new (v3 HOME of C38). Replaces v2 10:39 (Proposition 4's scope), since "Proposition 4" may not appear in the main text (V3-S6; `checks/terms.txt`) |
| 5 | The test configuration is one held-out severity between the two training severities (§6.2). | CAL-3 (β 0.43, 0.49, 0.70) | edited from v2 10:24 (item 2; "interpolated in one scalar ... no training data lies near criticality" cut for the budget; the β values live in §6.2) |
| 6 | The hazard is simple, with one ignition at reset, a one-step burn and no wind or uneven fuel (§3.1). | che/env/env.py:200-203 (reset: all-Fuel hazard with one random ignition); docs/theory_foundations.md Def. 3 as stated in paper/v3/sections/03_environment.md:49 (a Burning cell is Burnt one step later); DX-1 (ι = 0) | edited from v2 10:32 (item 10; "Corollary 1's exact critical value is specific to this idealized kernel" cut: the theory's scope lives in §3 and App. A). **Departure from the stub**: not in its ORDER list; kept because v2 carried it, no ruling removed it, and no other v3 section states it as a limitation (see Findings) |
| 7 | The only ablation of the death price is narrow, with three seeds, 500 updates and the fire as the only hazard (§3.3). | ENV-2 (scope note: "Pillar-only, 500 updates, 3 seeds"); ENV-3; ENV-4; ENV-5; che/bench/results/phase2/phase2_report.md:27-30 ("pillar-only training probe ... 500 updates each") | edited from v2 10:26 ("The only $d_p$ ablation is narrow and was not re-run under the protocol of §9 (§3.3)"): the scope is stated (stub), the "not re-run" clause cut for the budget; "pillar-only" in plain words |
| 8 | The task needs no coordination, the agents share one set of parameters, and no heuristic or scripted baseline is reported (§1). | ENV-6; ENV-9; ENV-11; paper/v2/sections/10_limitations.md:25, :31 | edited from v2 10:25 (item 3) and 10:31 (item 9); "swarm" dropped (`checks/terms.txt`) |
| 9 | We compare fixed training distributions and evaluate no adaptive curriculum. | decision log, READS RULING (docs/decision_log.md:5732), item 4 (:5772-5773: "§10 states that no adaptive curriculum is evaluated") | edited from v2 10:31 (item 9, "No external baseline, domain-randomization schedule or adaptive curriculum is evaluated") |
| 10 | Arms trained on different GPUs are marked where they are compared (§6.3). | HW-4; DX-5 | edited from v2 10:30 (item 8): the GPU blocks become a pointer (stub; their home is App. D, the short form §6.3; "GPU 1/2/3" are banned in the main text) |

## Findings

- **Departure (row 6).** The hazard-simplicity line (v2 item 10) is not in the
  stub's ORDER. I kept it in one sentence because an environment paper's
  referee will ask (P3's lens) and no other v3 file states it as a limitation;
  the owner may cut it (v2 wording for revert: "The hazard is simple: a
  one-step burn time, a single ignition at reset, no spontaneous ignition
  ($\iota = 0$), and no wind or fuel heterogeneity.").
- **No v3 home found** for v2 10:28 (item 6: the observation includes the
  agent's own position and time step; the wall-drift artifact, which no
  differenced test can see). §5 carries the "recorded, not graded" rule, but
  the artifact itself has no main-text home in the v3 stubs I read. For B1 /
  the orchestrator: decide whether §3.5 or §5 should carry it.
- **Word budget.** 201 prose words against 200.
