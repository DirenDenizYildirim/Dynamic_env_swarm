# RC1: claims review, part 1 (snapshot draft1)

Reviewer RC1 (claims lane), Paper v2 phase 1, step 4, pass 2, 2026-10-11.
Snapshot reviewed: `paper/v2/snapshots/draft1/sections/` (the live
`sections/` and `provenance/` were byte-identical to the snapshot when I
read them). `front_matter.yaml` is not snapshotted, so I reviewed the live
copy. Line numbers below are snapshot line numbers.

## Summary

**Counts:** 3 MUST, 1 OWNER, 35 SHOULD (39 findings).

**The MUST items**
- RC1-1: the disclosure footnote leaves out uses of the LLM that the record
  documents. The most important is that the LLM agent drafted the
  registered Phase-6 design whose error the paper owns. The provenance row
  also says the footnote "lists every use the record documents", which is
  false.
- RC1-2: "We checked every word" is not true of this draft. It becomes true
  only after the owner's check.
- RC1-9: the hero caption calls the "true state" panel perception. That
  breaks the state-versus-perception distinction the sentence exists to
  draw.

**The OWNER item**
- RC1-3: Q4h assumes the record names no author for the 2026-08-16 review.
  In fact the record indicates that a builder (LLM) session wrote both that
  review and the registered design it reviewed.

**Scope.** The abstract, hero, §1–§7 and the four alternates, plus the
title candidates, the `description` and `provenance/00_abstract.md`. I read
§8–§11 and the appendix for consistency only, and report from them only
where they conflict with my files (RC1-18, RC1-39).

**Method**
- **What I read:** the owner's prompt (`paper_v2_prompt.md`, including the
  fix list at :93-221); the log's DEMONSTRATION DRAFT and PAPER V2 entries
  and the tail entries they rest on; `BRIEF.md` in full; `FINDINGS.md` in
  full; `STRUCTURE.md` §3–§5; `plans/P3.md` §6; `review_of_demo.md` (by
  reference); every provenance file in scope.
- **Provenance:** for each sentence in the 100 % set I opened the stated
  support: the ledger row or the supplement or proposal row, the log entry
  at its lines, the code or test at file:line, and `RWV` Part 3 or
  `citations/*.md` for each citation use.
- **Scratch scripts** (`scratchpad/RC1/`):
  - a ledger-ID lookup across the ledger, the supplement and the
    `ledger_proposals`;
  - a scan for LLM-style patterns;
  - a jargon scan of body text, with STUB-SPEC blocks and code fences
    excluded;
  - an abstract word and character count, plus the title lengths;
  - a `yaml.safe_load` of the front matter;
  - a check of every `d-cite` key against `paper/v2/assets/bibliography/submission.bib`.
- **Kit facts:** read from this session's `out/kit_checks.md`. I did not
  run the kit build.

**Coverage**

| scope | sentences or rows checked against their stated support |
|---|---|
| abstract | 16 of 16, plus the footnote's 2 of 2 |
| hero | 9 of 9 |
| `description` | 1 of 1 |
| title candidates | 5 of 5 |
| §1 | 69 of 69 rows (62 that make a claim) |
| alternates | diffed against their defaults; `alt/00_hero.ladder.md` 12 of 12 rows |
| §2 | about 46 of 58 claim rows (every citation use) |
| §3 | about 38 of 93 |
| §4 | about 30 of 46 |
| §5 | about 26 of 47 |
| §6 | about 30 of 58 |
| §7 | about 30 of 43 |

In §2–§7 I gave priority to every class-B or "new" row, every row that
cites the decision log, and every citation key.

## Findings

| ID | severity | file:line | quoted text (short) | problem | evidence | proposed fix | class |
|---|---|---|---|---|---|---|---|
| RC1-1 | MUST | `00_abstract.md:24` (footnote); same text at `alt/00_abstract.no_recommendation.md:9` and `alt/00_abstract.disclosure_line.md:15`; `provenance/00_abstract.md:20` | "under our rulings it implemented the environment, training and analysis code, built the figures, helped search the literature, verified the citations, and drafted this text" | The footnote is not accurate against the record. It omits uses the record documents, and those uses bear on TMLR's "human-sourced" expectation. In the record, the LLM agent: (a) drafted the registered Phase-6 design, its red team and the remedies the owner adopted; (b) wrote the 2026-08-16 review that identified the inert-share bias and proposed ISO-4; (c) co-decided locks and issued recommendations that rulings adopted; (d) ran the measurements and analyses; (e) supplied LLM summaries alongside the owner's read of Gao et al. The provenance row's claim that the footnote "lists every use the record documents (P3-N23)" is therefore false. The record also does not show that every relay ("RA relay"; an "independent external assessment") came from Claude. | `phase6_design_v2.md:13-15` ("drafted by the same agent that produced the red team and proposed the remedies it now adopts"); `phase6_redteam_v1.md:3` ("Reviewer: RA (internal)"); `phase6_redteam_remedies.md:8` ("RA proposal"); log:3557-3560 (the venue review is "an assessment written this session from the repository"); `docs/venue_review_2026-08-16.md:22-26`; log:3652-3655 (its proposals 0–1 are the bias registration and ISO-4); `severity_lock.md:3-5` ("Decided jointly (owner + RA) … independently recomputed by the RA"); log:233, :1065 ("human + RA"); `kappa_b_lock.md:303` ("RA recommendation"); log:276 ("The RA measured"); `phase6_framing_allocation_ruling.txt:2, :5-6`; log:5709 ("with LLM summaries alongside"); `plans/P3.md:225` (N23: "RA" is the LLM coding agent); BRIEF §12 ("as the record documents each use") | The wording is the owner's (Q16). The default must still not present a partial list as complete. For example: "We used the LLM assistant Claude as a tool. Under our direction it drafted design documents and reviews, among them the review that identified the inert-share bias, proposed options on which we ruled, implemented and ran the code, analyses and figures, helped search the literature and verify citations, and drafted this text from our records." Correct provenance row 2, and add the open question of whether every LLM-assisted step was Claude. Mirror the change in both abstract alternates. | B (BRIEF §12 accuracy); wording C (Q16) |
| RC1-2 | MUST | `00_abstract.md:24`; `alt/00_abstract.no_recommendation.md:9`; `alt/00_abstract.disclosure_line.md:15` | "We checked every word and are responsible for it." | The statement is false of the draft as it stands. W1's own provenance says it is "true only once the owner's word-by-word check is done". Responsibility, by contrast, holds now (TMLR policy; PAPER V2 item 1). | `provenance/00_abstract.md:21, :113-115`; log:6047-6052 (the owner checks every word); log:6055-6056 | Until the owner approves the abstract, write "The authors are responsible for every word." The owner adds "We checked every word" at approval. Alternatively, keep the sentence behind a gate: an `OWNER-GATE` comment that `build_v2.py --final` refuses to pass. | B (every claim traces to the record); owner gate |
| RC1-3 | OWNER | `00_abstract.md:26` ("This is our design error … found before the main training runs"); `01_introduction.md:40` ("A review of the registered design identified the bias on 2026-08-16") | "A review of the registered design identified the bias" | Q4h rests on the premise that "the record calls it a review of the registered design and names no author". The record indicates otherwise. A builder (LLM) session wrote the 2026-08-16 review. The registered design it reviewed was drafted by the same agent that red-teamed it, and so was the framing registration. This is not an error in the text: "our design error" is right, since the authors are responsible. It is a new fact for three of the owner's decisions: Q4h (attribution), Q16 (the footnote's scope), and whether the paper should say an LLM-assisted review found the bias. | log:3557-3560; `docs/venue_review_2026-08-16.md:22-26`; `phase6_design_v2.md:13-19`; `phase6_framing_branches.md:13-14` ("by the same author with the same limited standing"); `FINDINGS.md:207` (Q4h's premise) | Put to the owner with Q4h and Q16. One option: §1 and §9.1 say "a review of the registered design, written with the LLM assistant, identified …", and the footnote names design drafting and review (RC1-1). The default text may stay as it is until the owner rules. | C (new) |
| RC1-4 | SHOULD | `00_abstract.md:28` | "each stressor is a parameter of one transition or observation kernel, so ablations are bitwise-exact nested models" | The "so" gives an incomplete reason. Parameterization makes an ablation a nested model. Bitwise exactness needs the engineering rule that every draw is made whether or not the stressor is on, which is how §3.4 and §11 explain it. | `03_environment.md:192, :202` ("One engineering rule makes the nesting exact"); `11_reproducibility.md` line 2 of its body; `CLAUDE.md` invariant #3; TF §8 table | "…each stressor is a parameter of one transition or observation kernel whose random draws are made whether or not it is on, so ablations are bitwise-exact nested models." That adds 10 words; the budget is already 12–14 over (Q20). If that is too long, write "…kernel, and switching one off reproduces the nested model bit for bit." | B (claim stronger than its support) |
| RC1-5 | SHOULD | `00_abstract.md:24` | "Both arms train at matched compute"; "the third, communication denial, is independent" | No arm has been named when "Both arms" appears. "Joint training" first appears in paragraph 2 without introduction. "the third" presupposes a count. `STRUCTURE.md` §4 move 1 asked for the labels "(JOINT)" and "(ISO)" in the opening. | `STRUCTURE.md:120-123` | In sentence 1, write "…whether training one policy on co-occurring stressors (joint training) beats training it on each in isolation (isolated training)…". Change "Both arms" to "Both" and "the third" to "a third". | — |
| RC1-6 | SHOULD | `00_abstract.md:26` (also `:24`) | "so the third of the isolated arm's training episodes that carry only it are fire-only"; "outside the confirmatory family"; "before unblinding" | "the third … that carry only it" presupposes something the reader has not been told, namely that a third of ISO's episodes carry only denial. "Confirmatory family" and "unblinding" are not defined at abstract level; BRIEF §5.2 defines both in §9.1. | BRIEF §5.2 rows "family" and "unblind"; DES-8 | "…so the third of the isolated arm's training episodes that carry only communication denial are, in effect, fire-only." Change "outside the confirmatory family" to "outside the two registered tests". Keep "unblinding", since it is standard in preregistration, or gloss it once in §1 (RC1-22). | — |
| RC1-7 | SHOULD | `00_abstract.md:26` | "CI [0.47, 1.44]" | BRIEF §10 requires "+ on positive interval ends", and §1:51 writes "[+0.47, +1.44]". The form also differs between the abstract and §1. (Numbers lane; noted here as a cross-section inconsistency.) | BRIEF.md:582-584; `01_introduction.md:51` | "[+0.47, +1.44]", in the abstract and both abstract alternates. | B (BRIEF §10) |
| RC1-8 | SHOULD | `00_abstract.md:24` (footnote) | "under our rulings … from our recorded rulings and results" | "Rulings" is project-internal vocabulary. A reader of page 1 cannot tell what a ruling is. | BRIEF §5.2 (process vocabulary) | "under our direction … from our recorded decisions and results". | — |
| RC1-9 | MUST | `00_hero.md:18` | "Perception is only in the selected agent's three panels: its observation as produced …, the true state of those cells, and P(seen) = τ" | As written, the sentence calls the true-state panel perception. The sentence exists to keep environment state apart from perception (DESIGN F1 risk 3), and it puts state inside perception. | STUB-SPEC `00_hero.md:7` ("only the selected agent's three panels are perception"; DESIGN F1 risk 3); `paper/figures/interactive/MANIFEST.md:93-98` | "Only the selected agent's three panels concern perception: its observation as produced (labelled obs v3, the masking observation), the true state of the same cells for comparison, and P(seen) = τ, the transmittance through smoke." That adds 2 words; to stay at the 100-word cap, cut "One episode of CHE." | B (accuracy) |
| RC1-10 | SHOULD | `00_hero.md:18` | "Configuration, episode key, random policy and stochastic actions were fixed before rendering." | It does not say which configuration. The print companion's include caption gives no rule, and the figure's subtitle is the only place θ\* appears. | ENV-13; STUB-SPEC `00_hero.md:7` (selection rule in one clause) | "The held-out configuration θ\*, the episode key, the random policy and stochastic actions were fixed before rendering." That adds 3 words; offset them under RC1-9. | — |
| RC1-11 | SHOULD | `00_hero.md:25`; `alt/00_hero.ladder.md:18` | "Each caption carries a status: illustrative …; registered …; sensitivity arm …; secondary …; descriptive …; reference scale (cross-artifact)…" | The list reads as the full vocabulary, but captions in my scope also use other statuses. These include "configuration facts" (Fig. 2), "schematic, no data" (Fig. 4), "calibration, no agents" (Fig. 5) and "trained policies, 500 updates" (Figs. 6–8). | `01_introduction.md:31`; `03_environment.md:27`; `04_severity.md:26`; `05_coupling_a.md:25`; `06_coupling_b.md:76, :90` | "Each caption carries a status. The recurring ones are: …", or add the extra terms. | — |
| RC1-12 | SHOULD | `alt/00_hero.ladder.md:11` | "JOINT is joint and ISO isolated training"; "The full ladder is Figure 11 (§9.2)." | The first is an elliptical gloss that reads as circular. The second uses "ladder" as the caption's own noun, although BRIEF §5.2 replaces it. | BRIEF §5.2 row "ladder (the figure)"; `01_introduction.md:44` (the default caption's form) | "JOINT trains one policy on every stressor at once, ISO one on each stressor alone; the figure's note defines ISO-4." and "The figure's “full ladder: §9.2” points to Figure 11." | — |
| RC1-13 | SHOULD | `provenance/00_abstract.md:57, :59` (T2, T4) | T2 "a pre-registered test whose survival gain does not survive the inert-share correction"; T4 "joint versus isolated training on co-occurring stressors" | T2 gives the gain to the test; the gain belongs to joint training. T4 departs from the ratified wording, and "isolated training on co-occurring stressors" misdescribes ISO. F1 says to keep the ratified terminology. | log:5610-5619 (the ratified title, "training on co-occurring versus isolated stressors"); `FINDINGS.md:44` | T2: "…, a pre-registered test in which joint training's survival gain does not survive the inert-share correction". T4: "A pre-registered test of training on co-occurring versus isolated stressors, in a multi-agent environment with an ambient fire hazard". | A (F1) |
| RC1-14 | SHOULD | `01_introduction.md:21` | "we study it for survival in multi-agent reinforcement learning" | This understates the test. It has two co-primaries, and completion is the founding primary. The owner's sentence had a following clause, "in an environment where agents are killed by fire and by structural collapse", which gave "survival" its sense; v2 cut it. | DES-13; `09_compositional_test.md:32`; `paper/finale.md:28-31` | "we study it in multi-agent reinforcement learning, for survival and task completion under a lethal fire". | — |
| RC1-15 | SHOULD | `01_introduction.md:40` | "At the test's severity, Coupling B's own survival effect in calibration was within the spread over three seeds (§10)." | The limitation is stated without its consequence, at the end of the paragraph on the δ design error. The reader cannot see why it matters. | `branch_B.md:178-181` (honesty line 5); `10_limitations.md` item 1 | "At the test's severity Coupling B alone had shown no survival effect beyond a three-seed spread in calibration, so the composition is tested where one of its two couplings is behaviourally quiet (§10)." | — |
| RC1-16 | SHOULD | `01_introduction.md:53` | "Once the active share is matched, JOINT's remaining differences add nothing detectable to survival, although it still sees each coupling twice as often …" | This restates Γ₄'s null from two sentences earlier, which is P3 §6's restatement pattern. "Add nothing detectable" also reads as stronger than the preceding "excludes only a large composition effect". | `plans/P3.md` §6 ("restating the same result"); RES-6 | Delete the sentence. End the Γ₄ sentence with "…, although JOINT still sees each coupling twice as often as ISO-4 and always in combination; a same-GPU replicate, proposed after Γ₄ was seen, agrees." | A (LEN) |
| RC1-17 | SHOULD | `01_introduction.md:55` | "In the search described in §2 we found no reinforcement-learning comparison that matches its arms on that share." | This sits uneasily with §2's account of Erdem & Üre: every attacked arm is attacked at every step, and "no arm has a counterpart of the fire-only share". On that account their attacked arms all have active share 1, so they are matched by construction. The scoop record behind the sentence predates the full read. | `02_related_work.md:45`; `RWV`:883-887 (abstract-level, "no full-text reads"); `RWV`:949, :1042-1045 | "In the search described in §2 we found no joint-versus-isolated comparison in reinforcement learning, with the isolated arm trained on a mixture, that controls that share; in the nearest, Erdem & Üre (2025), every attacked arm is perturbed at every step, so the share is fixed by design (§2)." Or drop the sentence. | — |
| RC1-18 | SHOULD | `01_introduction.md:51` against `09_compositional_test.md:32` | "The founding hypothesis, that joint training improves both outcomes, did not occur." against "task completion, the founding primary, on which the founding hypothesis was Γ(θ\*) > 0" | The paper defines the founding hypothesis two ways: on both co-primaries (§1; branch A, "founding registration") and on completion alone (§9.1; App. E calls A_c "the founding claim on the founding primary"). Both "did not occur" statements hold, but the definitions differ. | `phase6_framing_branches.md:101`; `paper/branch_B.md:231`; `14_appendix_plan_provenance.md:100, :104` | Keep §1, which matches branch A and `branch_B.md:231`. In §9.1 (RC2/W6), write "task completion, the founding primary, and survival rate", dropping "on which the founding hypothesis was Γ(θ\*) > 0", or name it "the original hypothesis". | — |
| RC1-19 | SHOULD | `01_introduction.md:60` | "A measurement protocol gives acceptance bars floors measured per metric, per GPU and per artifact" | The double object, "gives acceptance bars floors", is a garden path on first reading. | — | "A measurement protocol in which acceptance bars have floors measured per metric, per GPU and per artifact, and which names the bars that lack one (§8)." | — |
| RC1-20 | SHOULD | `01_introduction.md:61` | "…whose survival advantage does not survive the inert-share correction, registered before unblinding." | "registered before unblinding" dangles: it can attach to the test, which was pre-registered, or to the correction. | DES-12 against DES-15; P1-N3 | "…does not survive the inert-share correction, which was registered before unblinding." | B (P1-N3 scope) |
| RC1-21 | SHOULD | `01_introduction.md:44` (Figure 3 caption) | "Survival: Γ REJECT; Γ₄ null, “does not survive the inert-share correction”." and "X₄ is Γ₄'s minimum detectable effect" | Set beside "Γ₄ null", the registered string reads as if Γ₄ were what fails to survive. The registered qualifier is about the survival gain, Γ. X₄ is printed for completion only. | log:4987-4993; RES-6; the alternate hero's correct form (`alt/00_hero.ladder.md:11`) | "Survival: Γ REJECT; the gain “does not survive the inert-share correction” (Γ₄ null)." and "X₄, printed for completion, is …". To stay at the 120-word cap, change "The text quotes these rate differences × 100" to "The text quotes these × 100". | B (registered reading) |
| RC1-22 | SHOULD | `01_introduction.md:38` (first use; also :40, :55, :61) | "(a fifth was added before unblinding; Appendix E)" | "Unblinding" is used four times in §1, and in the abstract and hero, before §9.1 defines it. | BRIEF §5.2 row "unblind, unblinding"; `09_compositional_test.md` (§9.1, the "pre-unblind rulings" paragraph) | Gloss it at the first use in §1: "before unblinding, the first computation of any outcome contrast". | A (F5) |
| RC1-23 | SHOULD | `02_related_work.md:45` | "Of their six training arms, one is an unattacked baseline, … No arm has a counterpart of the fire-only share our correction removes." | "No arm" sits awkwardly right after naming an unattacked arm. The full read also records "every arm perturbed at every step" as an inference only: the attack's capped magnitude may be near zero, and the paper does not report it. | `RWV`:949; `RWV`:1042-1045 ("no scheduled clean steps, the output is a capped magnitude that may be near zero (unreported)") | "No attacked arm schedules clean steps, so none has a counterpart of the fire-only share our correction removes." | A (OI-3 accuracy) |
| RC1-24 | SHOULD | `02_related_work.md:43` | "and the strategy that covers more combinations does better"; "ours matches compute and, in the ISO-4 correction, the active share (§1)" | The full read records Stair as "generally the most effective", and the link to coverage as the authors' hypothesis. Separately, the record notes that in Gao et al.'s real-robot L-versus-Stair pair the share of demonstrations departing from the base setting is equal (15/16) by construction, which is the imitation-learning analogue of the active share. The juxtaposition "ours matches … the active share" implies they do not. | `RWV`:948; `paper/writing_drafts.md:1321-1324` (builder finding 11(a)) | "…and the strategy that cycles through factors is generally the most effective, which the authors attribute to its coverage of combinations." Then: "Our correction matches compute and the active share (§1); their real-robot pair also holds equal, by construction, the share of demonstrations that depart from the base setting." Or drop the "ours matches" clause. | C-adjacent (owner's final §2; READS RULING) |
| RC1-25 | SHOULD | `02_related_work.md:47` | "Theorem 1 (§6) is kin to the construction of their Proposition 1 … Chen et al. therefore do not subsume Theorem 1" | The "therefore" lost one premise: the owner's "but not covered by it", that is, Proposition 1 does not establish linear shortfall for a terminal-reward toy that can reveal the corridor. v2 cut it, which leaves "do not subsume" resting on the upper bounds and the different gap. | `paper/finale.md:330-335`; `RWV`:1046-1053 | "Theorem 1 (§6) is kin to the construction of their Proposition 1, …, but not covered by it: a terminal-reward toy that can reveal the corridor before the branch is not shown a linear shortfall." | — |
| RC1-26 | SHOULD | `02_related_work.md:39` | "None of the JAX multi-agent benchmarks we surveyed, JaxMARL, Multi-Agent Craftax and Assistax, has an evolving…" | The appositive list splits the subject from its verb. The owner's word order was clearer. | `paper/finale.md:250-253` | "Among the JAX multi-agent benchmarks we surveyed (JaxMARL, Multi-Agent Craftax and Assistax), none has an evolving, spreading lethal hazard field or perception attenuated by a hazard." | — |
| RC1-27 | SHOULD | `03_environment.md:182` | "for states that differ only in fire, smoke or structure, every difference far from all agents" | The test confines fire and structure differences to cells Chebyshev-far (≥ 6) from every agent. Smoke "may still differ everywhere". | `che/tests/test_reward_independence.py:8-13` | "…for states that differ only in fire, smoke or structure, with fire and structure differences at least six cells from every agent, so that the alive transition is pinned equal". | B (accuracy) |
| RC1-28 | SHOULD | `04_severity.md:25-26` (first use), `:50`; then throughout §4–§7 | "locked levels"; "the observable band it was locked to" | "Locked" is never defined. BRIEF §5.2 says to define it once in §3 or §4 as "fixed (locked) before the main experiment, with its date". | BRIEF §5.2 row "lock, locked" | At `04_severity.md:50`: "…each level is the observable band it was locked to, that is, fixed with its date before the main experiment (§4.3; Appendix B)". | A (F5) |
| RC1-29 | SHOULD | `03_environment.md:158`, `:182`, `:233` | "The penalty prices an outcome, not the hazard."; "Two tests check clause (i)."; "survival is learned through two hazard-blind routes:"; "each agent's transitions are independent samples under the team reward" | These are P3 §6 patterns: an antithesis closer that restates "whatever its cause" from the same paragraph, and announced enumerations. The last sentence is unclear. | `plans/P3.md` §6 | Cut "The penalty prices an outcome, not the hazard." Write "One test asserts … The other kills …", without the count. For the last: "each agent's transitions enter the shared policy's update as separate samples, all under the team reward". | A (LEN) |
| RC1-30 | SHOULD | `04_severity.md:56`, `:66` | "All of them bracket Kesten's ½."; "so it can be outrun, barely." | A single estimate does not bracket a value; only the family's range does, [0.480, 0.513]. "Barely" is an aphoristic flourish. | DX-204; DX-6 | "Their range brackets Kesten's ½." and "…so an agent that moves every step can stay ahead of it." | — |
| RC1-31 | SHOULD | `05_coupling_a.md:25` (Figure 6 note) | "Status: trained policies, 500 updates; seed ranges" | The status covers the whole figure, but the bottom panel shows the two Proposition 3 runs, which had no agents. | `05_coupling_a.md:87`; DX-304 | "Status: trained policies, 500 updates, seed ranges (top) · no agents (bottom) · …" | — |
| RC1-32 | SHOULD | `05_coupling_a.md:99`, `:44`, `:97` | "so the policies do not avoid weak cells, which two seeds per arm only suggest"; "Igniting a cell is not among the agents' actions, but the fire is not independent of them."; "The fall happens upstream of the agents." | The first states a claim and then hedges it in a trailing clause. The other two are an antithesis closer and an aphoristic opener (P3 §6). | CA-7; `plans/P3.md` §6 | "…with the coupling on, which suggests, on two seeds per arm, that the policies do not learn to avoid weak cells." "Agents cannot ignite a cell, but where they stand changes collapse rates, and a collapse can seed fire." Merge :97's opener into the next sentence: "Across all nine measured cells, … the share of seeded ignitions inside an alive agent's crop stays in [0.164, 0.203]." | — |
| RC1-33 | SHOULD | `06_coupling_b.md:32` | "Beer–Lambert attenuation is the standard optical model for light through smoke." | An uncited general claim, and arguable for smoke, where scattering matters. No verified source in `RWV` covers it, and BRIEF §15 allows nothing new. | BRIEF §15 | Cut it, or write "Beer–Lambert attenuation is the extinction law of an absorbing medium." | — |
| RC1-34 | SHOULD | `06_coupling_b.md:72` (H3) | "6.4 The cost is paid in survival, at High" | The heading echoes branch B's registered headline ("composition is paid in agents, not task return"), which §9.2 says "no longer holds as worded" and which `branch_B.md` §8 forbids. N17 treats such echoes as class B. | `09_compositional_test.md` §9.2 ("no longer holds as worded"); `branch_B.md:225`; `FINDINGS.md:85` | "6.4 Survival cost at High severity" (an H3, not in the `toc`). | B (N17's class) |
| RC1-35 | SHOULD | `07_comms.md:21` | "in CHE it had no measurable effect (Figure 9)" | The claim is unscoped and close to the point-null wording that the stub and §7.3 avoid. The record's verdict is "INERT WITHIN MEASUREMENT RESOLUTION", with bars at about 50 % power, and DX-16 "does not claim a point null". | `phase5_report.md:962`; DX-16; V4-1; `07_comms.md:73, :77` | "in CHE, under a frozen message encoder, no effect of it cleared its measurement bar (Figure 9)." | — |
| RC1-36 | SHOULD | `07_comms.md:73` | "δ = 0 against δ = 1 moves completion by +0.38 points … and survival by −1.43 points" | The direction is unclear. The source's Δ is δ = 0 minus δ = 1 (0.7396 − 0.7358; 0.9188 − 0.9331), so the text is correct but easy to misread. | `phase5_report.md:975-978`; COM-4 | "Completion is 0.38 points higher and survival 1.43 points lower with links open (δ = 0) than with links denied (δ = 1), against bars of 7.99 and 2.60 points." | — |
| RC1-37 | SHOULD | `07_comms.md:77` | "With deaths priced, the null also says that the value returning when a qualifier fails is weak at this scale and this death price." | "The value returning" is unclear. "The null" also sits against line 73's "none of these results is a point null". | log:1083-1088 (the record's sentence) | "Because deaths are priced, Remark 2′(i) allows communication some value here; the measurements say that this value is small at this scale and this death price." | — |
| RC1-38 | SHOULD | across scope, counted in prose: abstract 2 (:26, :28); §1 4; §2 5; §3 5; §4 2; §5 9; §6 8; §7 9 | ", so …" consequence clauses (44 in total) | This is a recognizable cadence, with at least one per paragraph in most sections, and several "so"s assert an inference the text does not supply (RC1-4; `01_introduction.md:23` "so the arms differ only in what their training distributions show"). | `plans/P3.md` §6 (style patterns a referee reads as generated) | Writers vary them: split into two sentences, use "because" where the cause is the point, and delete a "so" that names no real inference. Priorities: `00_abstract.md:28`; `01_introduction.md:23`; `05_coupling_a.md:99`. | — |
| RC1-39 | SHOULD | `12_appendix.md:48` (RC2's file; conflicts with `04_severity.md:35-38`) | "a divergence rate taken from Corollary 1(3), which the paper does not state (§4.1)" | v2's Corollary 1 has two items, so "Corollary 1(3)" points the reader at an item that does not exist. | `04_severity.md:35-38`; `alt/04_severity.no_item4.md:16` | "…a divergence rate from a critical-exponent item of the formal specification's Corollary 1, which §4.1 omits". | A (C1 knock-on) |

## Checked and clean

### F1: title candidates
- None of the five candidates leads with the hazard-blind reward.
- Each keeps "stressor", "multi-agent", and "pre-registered" attached to the 2026-08-13 test. The one departure is T4 (RC1-13).
- Lengths, measured with `len()`: 109, 75, 171, 172 and 139 characters, as provenance states.
- `front_matter.yaml` parses with `yaml.safe_load`.
- **`description`:**
  - one line, 229 characters, with no `"`, no `: `, no backslash and no digit;
  - it restates the abstract's new opening (DESCRIPTION item 3);
  - the owner's line is kept as the revert option.

### F2: the abstract's order and registered strings
- The order is what was tested, then survival up, then completion as an exclusion with its bound ("excludes a joint-training gain larger than 0.66 points"), then the Γ(t) shape, then "The survival gain does not survive the inert-share correction." Then come the cause (δ inert), the design error, the correction and the contribution.
- "sign unstable over the final half" appears verbatim, on both co-primaries, together with "the last fifth" (RES-12) and "from 70 %" (RES-13).
- No sentence between the gain and the qualifier calls the gain composition.
- "At matched compute" is present. No "converged", "budget-robust", "no effect", "certified", "swarm", PBT, "finite Dec-POMDP", "one transition kernel" or "as predicted before measurement" appears anywhere in my scope.
- **Counts:** 374 words by my count (W1 counts 372; over the 360 budget, recorded as Q20); 2,457 characters; the longest sentence is 39 words.

### F3: the δ design error
The timeline in the abstract (:26), §1 (:40) and §7 (:79) matches BRIEF §7:
- δ closed as inert on 2026-07-30 (V6-2);
- the design kept it on 2026-08-02 (V6-3);
- the bias identified on 2026-08-16 (V6-1);
- the grid began on 2026-09-09 (DES-12);
- registered with ISO-4 on 2026-09-18, mid-grid and before unblinding (DES-15).

I re-read V6-1–V6-3 at their sources: `venue_review_2026-08-16.md:1, :11-14`; `phase6_design_v2.md:9-10, :30-33, :63, :69-71, :129-131`; log:1065, :3551, :3652. The error is owned plainly. There is no foresight phrasing ("registered as a bias", "caught it"), "pre-registered" is never used for the correction, and §7 ends on a neutral pointer.

### F4: the recommendation
- The abstract's last sentence is labelled ("We recommend, from this single environment, …") and no "therefore", "so" or "thus" precedes it.
- §1 has no imperative: it states the confound's logic and points to "(§9.3)".
- The contributions list holds no "rule".
- §9.3's wording agrees with the abstract's.

### F5: jargon in my files
- "card", "rung", "ladder" and "unit" appear only as glossed printed labels (`01_introduction.md:44`).
- "obs v3" is glossed (`00_hero.md:18`), and "m44"/"m35" are glossed (`05_coupling_a.md:25`, `06_coupling_b.md:76`).
- Milestone codes appear only inside byte-identical listings and as printed labels named in captions.
- Exceptions: RC1-6, RC1-22 and RC1-28.

### C1: Corollary 1
- No 43/18, 4/3, "∼", universality claim or divergence on the arena remains.
- Corollary 1 item 2 matches Garet & Marchand's Corollary 5.4 as `citations/C1_verification.md:252-258` and :266-289 record it: conditioned on the infinite cluster; almost-sure Hausdorff convergence; a convex compact set with non-empty interior and symmetric under coordinate permutations and reflections; speed dependent on direction.
- `alt/04_severity.no_item4.md` differs from the default only in the corollary.

### C2: Remark 1 (`03_environment.md:52`)
It matches `citations/theory_cites.md` §1:
- NEXP-hard, and NEXP-complete for horizon below the number of states;
- two or more agents;
- a worst-case result that says nothing about an instance.

The "(δ > 0) … multi-agent POMDP" clause is gone from §1 and §3.

### C3: Proposition 4
No "irreducible" anywhere in my scope. §1:55's sentence agrees with TF:636-643's honesty note.

### OWNER ITEMS 1–4
1. "As predicted before measurement" is gone. The corrected timing at `01_introduction.md:60` and `05_coupling_a.md:95` matches DX-9 and `e11_report.md:13-27`, :170-197. The prediction's wording, "Medium may be its peak", is quoted as the record words it.
2. "Finite Dec-POMDP" appears only with the reachable-set qualifier (`01_introduction.md:23`, `03_environment.md:48-50`).
3. Erdem & Üre (`02_related_work.md:45`) is accurate to `RWV`:1042-1045, apart from RC1-23. N15's "at least as well … in all six cells, one a tie" is right.
4. §2 points to §5.1, and `05_coupling_a.md:44` gives CA-9's ranges with their scope (the Coupling-A grid's trained policies; random policies, as increase and as share). §2 provenance flags each changed sentence as needing a transcribed ruling (Q4a, RV-R1).

### N9–N11
- **N9:** "transition or observation kernel" appears in the abstract.
- **N10:** both registered strings are verbatim and the exclusion bound is added.
- **N11:** B̂ is omitted from the abstract and appears in §1 as "an estimate with no registered test".

### Honesty lines
- `branch_B.md` §5 lines 1–8 and 10 land where BRIEF §6.2 assigns them in my files. Line 5 (Medium siting) is at `06_coupling_b.md:80` (home) and `01_introduction.md:40` (one clause).
- Bias (b) is absent from §1, as Q21's default has it (FINDINGS P3-§2). BRIEF §6.1 lists "§1 (one clause)", so the two scaffold files disagree; the Q21 default governs.

### Citations
- Every one of the 40 keys used in my scope is in v2's `submission.bib` (41 entries). Uses checked against BRIEF §15 and `RWV` Part 3: `haksar2018`, `cakir2025jaxwildfire` (§2, §3.3), `garcia2015safe`, `liu2026vulcan` ("baselines only", RWV:946), `raut2026psps`, `alomari2025macraftax` (lava impassable), `hafner2022crafter`/`matthews2024craftax` (±0.1 per health point), `pynadath2002` (Theorem 4 / Theorems 5–6), `hu2025adaptablemarl` (v2-only quote), `bernstein2002`, `grassberger1983`, `kesten1980`, `garet2004chemical`, `gao2024composition` (RC1-24), `chen2022understandingdr` (RC1-25), `erdem2025mixed` (RC1-23), `agrawal2023multimodal`, `keysers2020`, `kirk2023zsg`, `crain2008stressors`/`cote2016stressors`/`zscheischler*`, `lu2022dpo`, `rutherford2024jaxmarl`, `dewitt2020ippo`.
- §2's search paragraph agrees with DX-101, with `RWV`:883-887 and Part 3, and with the footnote's "helped search the literature".

### Code and test facts (§3), read at source
- `env.py:159-173` (three stages, no PRNG);
- `env.py:241-243` (one ignition);
- `env.py:361`;
- `env.py:394-396` (the observation's own stream);
- `env.py:446-447` (completion = 1 − F/32);
- `test_lethality.py:143-162` (cause-blind);
- `test_nesting.py:78-88`, `:222-240`;
- `test_comms.py:272-319` (CPU digest from before comms existed).

All match, except the nuance in RC1-27.

### Record lines read at source
- `phase2_report.md:27-48` (the d_p ablation's scope, "last 50 logged updates");
- `phase5_report.md:960-980`;
- log:262-285 (κ_B = 1.0 locked 2026-07-27, as `06_coupling_b.md:70` says);
- `severity_lock.md:3-15` (`04_severity.md:56`'s provenance sentence is accurate).

### Double-blind
My files contain no names, URLs, hashes or absolute paths. The footnote names the tool only.

In-prose code paths in §3 presuppose readable code. That is the known N14/Q4e question, not a new finding.

### Alternates in step
- `alt/00_abstract.no_recommendation.md` differs only by the last sentence.
- `alt/00_abstract.disclosure_line.md` differs only in moving the footnote to a visible italic line.
- The reading note in `alt/00_hero.ladder.md` is identical to the default's.

### Kit placement of the footnote
From `out/kit_checks.md:95-96`, this session's B2 build, which I did not run:
- the marker's sentence prints on page 1;
- the footnote text prints on page 47 of 50.

The default therefore does not put the disclosure text on the first page in print. That is still Q4f, not a new finding.
