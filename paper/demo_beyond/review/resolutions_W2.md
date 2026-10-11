# Resolutions — W2 (`sections/03_environment.md`, `sections/04_severity.md`)

Fix round, 2026-10-11, under `review/DECISIONS.md`. Line numbers are the
post-fix files'. No code was run; only my two section files and
`ledger_proposals/W2.md` were edited.

| id | action | where / why |
|---|---|---|
| C-8 | fixed | 03:32. The proof's argument is kept (DECISIONS 3) and now names why: "The state space itself is not, since $\mathcal{P} = \mathbb{R}_{\ge 0}^G$ is not a finite set; but …". App. A is W4's file (C-32) |
| C-9 | fixed | 03:143. Now reads "only through the transition and observation kernels, never through the reward", followed by what each kernel does |
| C-10 | fixed | 03:186. Now reads "a stream derived from the reset or step key by a fixed tag" (the mixture draw folds the reset key, `env.py:221`) |
| C-11 | fixed (kept as is) | 03:222. The keeper adjudicated the sentence as correct; no change |
| C-12 | fixed | 03:125. The three-stressor preview is now one sentence with pointers to Definitions 5–7 and §§5–7. Its locked values, and the CA-1, CB-1 and COM-6 tags, left §3 because §§5–7 give them |
| C-13 | fixed | 04:25. Now reads "CHE's fire kernel on its own is the idealized kernel on a finite arena (Coupling A adds ignitions; §3.2)" |
| N-16 | fixed | 04:43. "L = 64" and "512 seeds" retagged DX-7 |
| N-17 | fixed | 04:9 (Fig. 5 caption). Added the DX-202 tag after "episode key 0". DX-202's value in `ledger_proposals/W2.md` now includes the render rule (random policy, `PRNGKey(0)`; `MANIFEST.md:314-317`). Numbers said DX-202's config lines were 1–2 off; `grep -n` shows them exact (low :30/:44/:54, medium :33/:47/:58, high :32/:46/:57), so they are unchanged |
| M-5 | fixed | 03:28. Followed DECISIONS 6: γ_p and γ_n keep their names. One sentence says "an unsubscripted $\gamma$ is always this discount, while the subscripted $\gamma_p$ and $\gamma_n$ of §9 are the secondary design's slopes; Corollary 1 (§4) writes its critical exponents as numbers". The γ in Def. 1's tuple stays, for fidelity to TF Def. 1 (mechanics wins on theory fidelity) |
| M-7 | fixed | 03:13. Under DECISIONS 6, the agent count is the "other" n, so it loses the letter: "a finite set of agents $I$". §3.5 states the instance's 12 agents in words. §9's n (the fire-only share) is the only n left |
| M-13 | fixed | 03:9. Dropped the duplicate `<strong>Figure 4.</strong>`, so the label is now only in the include caption, as in Figs. 7–9. Appended `<span class="figure-note">Status: schematic, no data · Interact: none (static figure).</span>` |
| M-21 | fixed (the part on my files) | 03:230. The budget sentence now says "(a training budget, not the episode horizon $T$)". T\* is the registered name, so it stays. Every other overload this finding lists is outside my files |
| M-22 | fixed | 04:18. Added "(Proposition 2, whose coupling holds on any graph, in particular $\mathbb{Z}^2$)" |
| M-23 | fixed | 03:30. Prop. 1 is now titled "(Well-posedness and Markov closure)", matching App. A and TF's "Well-posedness / Markov closure" |
| M-32 | fixed | 03:36, :115, :143, :230; 04:20. Every citation is now "Author (year)<d-cite>". Remark 1 reads "Bernstein et al. (2002) show"; Prop. 2 reads "described by Grassberger (1983)"; Def. 2 reads "in JaxWildfire … Çakır et al. (2025) penalize"; training reads "de Witt et al. (2020) … Lu et al. (2022) … Rutherford et al. (2024)"; Cor. 1 reads "a theorem of Kesten (1980)". No characterization of any cited work was added beyond BRIEF §B4's permitted use |
| M-39 | fixed | 04:55. Split into: "That probe had saved no checkpoints, so it was re-run with the same configurations and seeds (equivalent, not bitwise identical), and the re-test evaluated its final checkpoints on 512 episodes each" |

**Checks after the fixes.** The three listings were re-diffed against their sources (byte-identical). There is no `$` in any raw-HTML block, and every line has a balanced `$` count. Liquid appears only in the two allowed forms. There are no bare underscores in prose, and no parenthetical "(Author, year)" citations remain. Prose words: §3 about 2,660 (C-12 cut a sentence, while C-8 and the M-5 and M-21 notation additions each added a clause); §4 about 1,290. No finding on my files was skipped.
