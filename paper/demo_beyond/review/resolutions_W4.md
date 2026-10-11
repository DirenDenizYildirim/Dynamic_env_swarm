# Resolutions — W4 (§9, §10, §11, Appendices), fix round 2026-10-11

Per `DECISIONS.md` item 10: one row per finding on W4's files. Files edited: `sections/09_compositional_test.md`, `10_limitations.md`, `11_reproducibility.md`, `12_appendix.md`; new verified rows DX-412…DX-416 (and DX-406's arithmetic note) in `ledger_proposals/W4.md`. No other file touched; no code run; no commit.

| id | action | where / why |
|---|---|---|
| C-22 | fixed | Fig. 11 figure-note: Γ₄ sensitivity arm; Γ₄′ "secondary (S5), non-verdict-bearing, read at z_α"; B̂ "no registered test". Results table Γ₄′ status "secondary (S5), same card, read at $z_\alpha$"; §9.2 Γ₄′ paragraph and §9.1 readings sentence say S5, proposed after Γ₄ was seen |
| C-23 | fixed | §9.2 Discussion uses the keeper's wording: remaining differences (twice the per-coupling frequency, full co-occurrence) add nothing detectable; an exclusion, a composition effect up to +0.63 points not ruled out |
| C-24 | fixed | §9.2 "Where the survival gap lives": the identity deaths = 12 × (1 − survival rate) stated, "descriptive and grades nothing", no causal verb; DX-406 now shows the unrounded input |
| C-25 | fixed | §9.1: "as the registration records"; pointer to §6 only |
| C-26 | fixed | §9.1 endpoint paragraph: JOINT also differs from every secondary arm in δ = 1.0, inert under this encoder at this scale (§7) |
| C-27 | kept | adjudicated; T = 2000 sentence kept (trimmed) |
| C-28 | fixed | Fig. 11 caption cut to row identities, marks and what it cannot show; prose CIs replaced by the table except the headline Γ and Γ₄ survival intervals; §9.1 readings table cut to three rows plus one sentence; secondary paragraph cut to the two predictions and the tension sentence, rest by pointer to App. I; blinding kept in §9.1, §11's copy cut (C-31). §9 prose ≈ 3,350 words (still above the 2,800 target: D9's required items) |
| C-29 | fixed | §10 "what the record adds": the three bullets now point to §9.2 instead of restating numbers |
| C-30 | fixed | §11: floors are measured because training is nondeterministic; tests use seed dispersion because a k-seed mean varies by seed too (§8) |
| C-31 | fixed | §11 "One look per stage" is one sentence pointing to §9.1 |
| C-32 | fixed | App. A Prop. 1: §3's reachable-set argument, plus one sentence that it departs from the formal specification's wording (S and Ω_i finite) because ρ is real-valued (DECISIONS item 3) |
| C-33 | fixed | App. A Prop. 3 note: "at both of M3.3's grid sizes", no grid-size number, CA-3 tag removed |
| C-34 | fixed | App. A: statements of Props. 1–4, Thm. 1 and Remark 2′ replaced by pointers to §3, §5, §6, §7, §9.1, proofs kept; Remark 2′ keeps only the lowest-depth asymptotic step (with $\tilde q$ defined); App. C ratios paragraph cut to its first sentence; App. E branch reading cut to one line. Appendix ≈ 5,470 words (was 6,260) |
| N-3 | fixed | as C-33 |
| N-4 | fixed | App. B observation version retagged DX-401 |
| N-5 | fixed | App. C M6.0 card retagged DX-5 |
| N-6 | fixed | App. C M6.2b "set the design k = 40" with DES-1, DX-402 |
| N-9 | fixed | App. H: every sd and CI cell tagged DX-24 / DX-25 |
| N-10 | fixed | App. I: in the plane the slope along the sweep is γ_p + γ_n; the sweep's own slope is a separate fit and need not agree (it does not on completion); table row labelled "separate OLS fit" |
| N-11 | fixed | App. D item 9 retagged to new DX-413 (ratified after unblinding, before the sweep was read; log:5005-5008, :5058-5063) |
| N-12 | fixed | §10 item 8: DES-3 after 72, DX-30 after the seed blocks |
| N-13 | fixed | App. D item 7 retagged to new DX-414 (design v2 §7, final-five ruling 4, 2026-08-02) |
| N-14 | fixed | App. F: DX-4 after the seed list |
| N-15 | fixed | App. C M5.5 rows retagged to new DX-412 (m55/provenance.txt:5, :8-9); the §7 instance is W3's |
| N-18 | fixed | App. I floors sentence tagged new DX-415 (secondary.md:61); the §8 instance is W3's |
| N-19 | fixed | App. B "(3 × 3 box)" dropped |
| N-20 | fixed | prose CIs that remain carry "Šidák-corrected 95 %" (Γ, Γ₄, $\Gamma_{H,4}$, Γ(750)); the others moved to the table |
| N-21 | fixed | §9.2: "`sweep_c50_p000` − ISO-4 … is −0.15" |
| N-22 | fixed | App. C: 0.0621; the §6/§8 instances are W3's |
| N-24 | fixed | my instances tagged: CAL-3 (arm table, biases, High), DES-3 (k = 72, Fig. 11 note, seeds 1–72), DES-1 (seeds 1–60), DX-416 (seed 0, new row, test_p6_grid.py:155-170), DX-5 (Fig. 11 units), DES-13 (table lead-in T\*), DES-7 (p = 1), DX-28 (p ≤ 0.5), RES-13 moved after "70 %", METH-1 (App. C δ = 0, R_comm 16), DX-412 (App. C 1000 updates), DES-9 (every μ, ν cell), ENV-6 (9 × 9) |
| M-1 | fixed | as C-32 |
| M-3 | fixed | App. A no longer restates Thm. 1; proof (2) says the signal-blind policy "is among the optimal ones", matching §6 |
| M-4 | fixed | Def. 8 keeps the specification's "expected episodic return"; one sentence says the test reads it on two outcome metrics; Prop. 4 stated for the γ-discounted return, and "it concerns return rather than the co-primaries" |
| M-5 | fixed per DECISIONS 6 | γ_p, γ_n kept; discount γ only in Prop. 4 / App. A / App. B; §3 (W2) carries the notation note, so §9's own note was dropped |
| M-6 | fixed per DECISIONS 6 | per-coupling marginal renamed μ in §9.1, Fig. 13 caption and App. I; Šidák keeps m; Prop. 3's statement no longer appears in App. A |
| M-7 | fixed per DECISIONS 6 | fire-only share renamed ν (§9, App. I; Fig. 13 caption notes the figure labels them m and n); App. C sample size in words / "reps" column |
| M-8 | fixed (my part) | §9.1 says X is the $\mathrm{MDE}_{80}$ of §8; §8.2's z_α′ is W3's |
| M-9 | fixed | §9, §10, App. B–E prose and tables use inline math ($\kappa_A$, $d_p$, $k_{\mathrm{req}}$, $A_c$, $R_L$, $f_{\mathrm{weak}}$, $R_{\mathrm{comm}}$, $\sigma_s$, $z_\alpha$, $\Gamma_H$); App. D verbatim quotes keep the record's text |
| M-16 | fixed | App. D: "T\* ruling, item 2/3", "the proposals ruling of 2026-09-18"; one sentence says a "§" inside a quotation is the record's own |
| M-18 | fixed | figcaptions: θ&#42;, T&#42;, κ<sub>A</sub>, γ<sub>n</sub>, γ<sub>p</sub>, z<sub>α</sub> |
| M-19 | fixed | arm and constant identifiers in backticks (Markdown) or `<code>` (HTML), outside verbatim quotes |
| M-20 | fixed (my part) | App. A defines Θ; Remark 2′ note defines $\tilde q$; §8.6's B̂ pointer is W3's |
| M-21 | skipped | T\* and T = 2000 are the registered budget names, and the other overloads sit in other writers' sections; no ambiguity inside §9–§12 that a reader cannot resolve from context |
| M-23 | fixed | App. A titles now equal §3/§5/§6/§9.1's ("Well-posedness", "Bond percolation", …, "An irreducible shift term for ISO") |
| M-24 | fixed | "(D1)" dropped; App. B "the death-penalty design decision", "the observation design decision"; §10 "the fire alone with no couplings … an earlier observation encoding" |
| M-25 | fixed | as C-25 |
| M-26 | fixed | App. I completion row: γ_p prediction +2.69 (γ_p × 1, DX-27) beside Γ₄ −1.26 and Γ₄′ −2.47; γ_n prediction "not drawn in Figure 13, and no value stated" |
| M-27 | fixed | as C-22 |
| M-29 | fixed | App. D intro: "emphasis is the record's own, one indented code line is set inline" |
| M-32 | fixed (my part) | "(de Witt et al., 2020)" → tag alone; "the DBCA method of Keysers et al. (2020)"; "Grassberger (1983)"; "Pynadath & Tambe (2002)" |
| M-33 | fixed | Fig. 11 and Fig. 12 alt texts "Šidák" |
| M-34 | skipped | reviewer: "fine as is" |
| M-36 | fixed | §10 "only because" |
| M-37 | fixed | §9.1 Prop. 4 text: "every state where both couplings act at once"; App. A's sentence removed with the restatement; "co-active" now names the counter only |
| M-38 | fixed | "towards" in §10 and App. J |
| M-41 | fixed | App. E row D: "− on either co-primary" in both metric cells |
| M-12 (J1) | fixed | App. J names Figures J1 and J2 before the first block, and J1 again directly before it |
