# Resolutions: W1 (step 4, pass 3, fix round)

Writer W1, 2026-10-12. Files: `sections/00_abstract.md`, `sections/00_hero.md`,
`sections/alt/00_abstract.no_recommendation.md`,
`sections/alt/00_abstract.disclosure_line.md`, `sections/alt/00_hero.ladder.md`,
`front_matter.yaml` (`title`, `description`), and their `provenance/` files.
Every changed sentence has its provenance row updated, with the finding ID in
the change column. The two abstract alternates were regenerated from the
fixed default, so they differ from it only as before (the recommendation;
the disclosure's placement). No number changed except the two `+` signs, so
no new ledger row.

Counts: **16 fixed, 2 declined, 5 owner.**

| finding ID | outcome (fixed / declined / owner) | what changed, or why not |
|---|---|---|
| RC1-1 (MUST) | fixed | Footnote rewritten under orchestrator decision 7: "We used the LLM assistant Claude under our direction; its uses included drafting design documents and reviews, proposing options for our decisions, writing and running the code, analyses and figures, helping with literature search and citations, and drafting this text from our records." "Included" means it is not presented as a complete list. It adds the design documents, reviews and proposed options the record shows (`phase6_design_v2.md:13-15`; `phase6_redteam_v1.md:3`; `phase6_redteam_remedies.md:8`; `kappa_b_lock.md:303`; `severity_lock.md:3-5`; log:276). It names no particular review, so it does not contradict RC1-3. Provenance row 2 corrected, with draft1's "lists every use" claim withdrawn. Mirrored in both abstract alternates |
| RC1-2 (MUST) | fixed | "We checked every word and are responsible for it." became "The authors are responsible for every word." That holds now (PAPER V2 item 1; TMLR as read, log:6055-6056). Mirrored in both abstract alternates |
| RC1-3 (OWNER) | owner | Recorded as open item 2(a) in `provenance/00_abstract.md`, for Q4h and Q16. The text is unchanged, and the footnote neither asserts nor denies who wrote the 2026-08-16 review |
| RC1-4 (SHOULD) | fixed | "…kernel, so ablations are bitwise-exact nested models" became "…kernel, and switching it off reproduces the nested model's trajectories bit for bit", in the owner's §1 words (`paper/finale.md:69-70`). The inference is gone |
| RC1-5 (SHOULD) | fixed | "Both arms train" became "Joint and isolated training are run at matched compute and evaluated…", so both arms are named before "Joint training" first appears. "The third" became the owner's "a third". I did not add RC1's sentence-1 labels: they would push sentence 1 past 40 words |
| RC1-6 (SHOULD) | fixed | The δ sentence no longer presupposes the third: "Communication denial, inert under a frozen random-projection encoder at this scale, is the only stressor in a third of the isolated arm's training episodes, which are thus fire-only in effect." "Outside the confirmatory family" became "outside the two confirmatory tests", the hero reading note's wording. "Unblinding" is kept, as RC1-6 allows |
| RC1-7 (SHOULD) | fixed | "[+0.47, +1.44]" (same fix as RN1-10) |
| RC1-8 (SHOULD) | fixed | "Rulings" is gone from the footnote: it now says "under our direction" and "from our records" |
| RC1-9 (MUST) | fixed | The hero caption now reads: "Only the selected agent's three panels concern perception: its observation as produced (…), those cells' true state, for comparison, and P(seen) = τ…". The caption stays at the 100-word cap |
| RC1-10 (SHOULD) | fixed | "The held-out configuration θ\*, episode key, policy and stochastic actions were fixed before rendering." |
| RC1-11 (SHOULD) | fixed | The reading note now starts "Captions carry a status; the recurring ones are…", in the hero and in the ladder alternate |
| RC1-12 (SHOULD) | fixed | Ladder alternate: "JOINT trains on all stressors together, ISO on each alone; …" and "Its “full ladder: §9.2” is Figure 11." Two small trims ("X₄: its", "registered (Γ)") hold the 120-word cap |
| RC1-13 (SHOULD) | fixed | Title candidates in `provenance/00_abstract.md`: T2 now reads "…a pre-registered test in which joint training's survival gain does not survive the inert-share correction" (191 characters). T4 now uses the ratified "training on co-occurring versus isolated stressors" (133 characters). The recommended title T1 is unchanged |
| RC1-21 (SHOULD) | declined | Not W1's file: it concerns §1's Figure 3 caption (W2). My ladder alternate already has the form RC1-21 proposes |
| RC1-38 (SHOULD) | fixed | Both ", so" clauses in the abstract are gone (`:26` under RC1-6, `:28` under RC1-4) |
| RC2-31 (SHOULD) | fixed | "[+0.47, +1.44]" (same fix as RN1-10) |
| RN1-10 (MUST) | fixed | "CI [+0.47, +1.44]" in the abstract and both alternates. The provenance keeps the owner's "[0.47, 1.44]" as the revert form |
| RN1-14 (SHOULD) | fixed | Γ₄'s interval is now labelled "Šidák-corrected CI [−0.68, +0.63]" (support: `post_gamma4_t2000.md:5`) |
| RM-4 (MUST, class C) | owner | The hero iframe `height` is left at 1100 by orchestrator decision 4 (B2 pins it in CSS; the orchestrator then sets the attribute). Recorded in `provenance/00_hero.md` |
| RM-6 (MUST, class C) | owner | The fix is B2's option-B build flag (Q8), not text. `provenance/00_hero.ladder.md` now marks the alternate as a caption draft, not a buildable page |
| RM-8 (OWNER) | owner | RM's print measurement, with options (a)–(c), is now open item 1 in `provenance/00_abstract.md` and item 1 in `provenance/00_abstract.disclosure_line.md` (Q4f) |
| RM-22 (SHOULD, class C) | owner | DESCRIPTION item 3 (log:5692-5693) requires the `description` to restate the abstract's opening. Changing that is Q4d; option B is recorded in the `description` table |
| RM-23 (SHOULD) | declined | Not W1's field: `date` is B2's placeholder and the owner's decision (Q2) |
