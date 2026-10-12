# Resolutions: W2 (§1 Introduction, §2 Related work), fix round, 2026-10-12

These are the findings in RC1, RC2, RN1, RN2 and RM that touch `sections/01_introduction.md` or `sections/02_related_work.md`, plus the orchestrator's decision 2.

- **Line numbers** cite `snapshots/draft1/`.
- **Provenance.** Every changed or new sentence has its row in `provenance/01_introduction.md` or `provenance/02_related_work.md`, and the row's change column names the finding.
- **Checks after the fixes.** `build_v2.py` finds no failure and no M1 flag in either file. It still fails overall, on two IDs in other writers' files (V4-3 in §7, V6-4 in §9). `provenance_check.py --strict 01_introduction 02_related_work` reports no unsourced sentence, no stale row and no support problem.
- **Ledger.** No new ledger rows.
- **Words (P3's method).** §1 has 1,174 prose words (draft1 had 1,123; the budget is 950). §2 has 1,313 (draft1 had 1,270; the budget is 1,150). The Figure 3 caption is 118 words against a cap of 120.

| finding ID | outcome (fixed / declined / owner) | what changed, or why not |
|---|---|---|
| RC1-3 | owner | Unchanged until the owner rules on Q4h and Q16. The finding: the record shows an LLM builder session wrote the 2026-08-16 review and drafted the design it reviewed. The open item is recorded in provenance/01 (Open items 7). |
| RC1-14 | fixed | 01:21 now reads "we study it in multi-agent reinforcement learning, for survival and task completion under a lethal fire" (DES-13: two co-primaries). |
| RC1-15 | fixed | 01:40 now gives the consequence in the record's words (§7 PROPOSALS RULING, log:4157-4160): "At the test's severity Coupling B was behaviourally quiet in calibration: its own survival effect was within the spread over three seeds (§6.4), and by the project's own locks no severity has both couplings strongly live (§10)." |
| RC1-16 | fixed | 01:53's "Once the active share is matched, JOINT's remaining differences add nothing detectable…" is cut as a restatement. Its "twice as often … always in combination" clause now ends the Γ₄ sentence, and the replicate clause is its own sentence. |
| RC1-17 | fixed | 01:55 is narrowed to what the search and the full reads support: "we found no reinforcement-learning comparison that trains its isolated arm on a mixture of single stressors and matches that arm to the joint one on this share". This agrees with §2: Erdem & Üre train no arm on such a mixture (RWV :1043). RC1's proposed wording was not used, because it relied on "perturbed at every step", which RWV marks as inference only (the point RC1-23 makes). |
| RC1-18 | declined | Nothing to change in §1. The finding keeps §1's definition, which matches branch A and `branch_B.md:231`; its proposed fix is in W6's §9.1. |
| RC1-19 | fixed | 01:60 now reads "Under the measurement protocol of §8, acceptance bars come with floors measured per metric, per GPU and per artifact, and the bars that lack one are named." This uses the owner's phrase "come with floors" (finale.md:170). |
| RC1-20 | fixed | 01:61 now ends "…does not survive the inert-share correction, which was registered before unblinding" (P1-N3). |
| RC1-21 | fixed | The Figure 3 caption now reads "Survival: Γ REJECT; the gain “does not survive the inert-share correction” (Γ₄ null)" and "X₄, on the completion row, is …". To stay under the 120-word cap, "Γ₄'s completion interval is drawn but not printed." is cut; §9.2's table gives the interval. |
| RC1-22 | fixed | "Unblinding" is glossed at its first use in §1 (01:38): "before unblinding, the first computation of any outcome contrast" (BRIEF §5.2). |
| RC1-23 | fixed | 02:45 now reads "…in each of the others an attack is computed at every step (their Algorithm 1). No attacked arm schedules clean steps, so none has a counterpart of the fire-only share our correction removes." (RWV :1044) |
| RC1-24 | fixed | 02:43 now reads "the strategy that cycles through factors is generally the most effective, which the authors hypothesize is due to the combinations it covers" (RWV :948). The clause "ours matches compute and, in the ISO-4 correction, the active share" is cut: their real-robot pair holds the departing-demonstration share equal by construction. Both changes depart from the owner's final §2 and are flagged as class C pending transcription (Q4a). |
| RC1-25 | fixed | 02:47 restores the owner's "but it is not covered by it" (finale.md:335). A new sentence gives the premise: "That construction obtains a shortfall growing linearly in the horizon from per-step rewards in absorbing states, while Theorem 1's two-corridor toy has a single terminal reward and can reveal the corridor before the branch" (RWV :1050-1053). |
| RC1-26 | fixed | 02:39 returns to the owner's word order: "Among the JAX multi-agent benchmarks we surveyed, …, none has …" (finale.md:237-240). |
| RC1-38 | fixed (in part) | RC1's priority site, 01:23, is fixed: "…, so the arms differ only in what their training distributions show the agents" now reads, in the owner's words (finale.md:46-48), "…; the agents meet the fire only through what they observe and what happens to them". At 01:25 ", so the three severities" becomes ", and the three severities". The remaining ", so" clauses (two in §1, four in §2) each state a real inference and are kept. |
| RC2-23 | fixed | Same fix as RC1-16. |
| RC2-32 | fixed | Same fix as RC1-20. |
| RN1-15 | declined | The tag on "the three severities" (01:25, CAL-3) is accurate, and BRIEF §10 errs toward tagging. Consistency is better reached by tagging the untagged counts, which are in W3's and W4's files. |
| RN1-16 | owner | Numerals that describe cited works in §2 ("six cells, one a tie", "six training arms", "one or two types") carry no tag. Their support is the RWV line in each provenance row. Whether such numerals are exempt is the owner's ruling; this is recorded in provenance/02 (Open items 6). |
| RM-6 | owner (Q8; B2's flag) | No text change in §1. §1 refers to figures by number only, so B2's option-B flag can renumber "(Figure 1)" at 01:25 and move the Figure 3 block mechanically. |
| RM-21 | owner (class C) | §2 keeps "Table 1". Numbering all 16 tables, or dropping the number, needs a ruling; this is recorded in provenance/02 (Open items 7). |
| RM-24 | declined (not in my files) | §2 already spells it "Tramèr". The reference list's "Tramer" is B2's fix, at `related_work_verification.md` and the bib (M2). |
| RM-26 | fixed | 01:40's pointer now goes to the home, "(§6.4)", with "(§10)" for the limitation; this was combined with the RC1-15 fix. |
| Decision 2 | fixed | 01:55 (now two sentences) reads "Proposition 4 (§9.1), a transfer bound for a fixed policy, bounds only what isolated training can be guaranteed to transfer." This is the C3 wording, with no "irreducible". |
