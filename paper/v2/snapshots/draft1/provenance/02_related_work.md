# Provenance: sections/02_related_work.md

Writer: W2 (Paper v2, step 4, pass 1). Checked against the section on
2026-10-11 with `paper/v2/src/provenance_check.py 02_related_work` (no
snapshot label taken). The demo is `paper/demo_beyond/sections/02_related_work.md`
("demo 02:<line>"); the owner's §2 is `paper/finale.md:180-370`, ruled final
under READS RULING (`docs/decision_log.md:5732`) and reopened for v2 by
PAPER V2 (`:6036`). Every characterization of a cited work stays within
`paper/related_work_verification.md` (RWV) Part 3 and the owner's §2; line
numbers are those of the working copy B2 edited for M2 (the quoted content
binds, `BRIEF.md` §0). "LEN" is the fix list's length item (class A).
Counted with P3's method (`plans/P3.md` §5): **1,270 prose words** against a
budget of 1,150 (the demo's 1,536), plus Table 1 (177 words in cells,
unchanged).

| # | sentence (verbatim) | support | change from the demo, and why |
|---|---|---|---|
| 1 | 2 Related work | framing | kept (STRUCTURE.md §2 heading) |
| 2 | Table 1 sets the nearest fire-related and safety-related work beside CHE. | framing | edited (class A, LEN; P3 §6): the demo's opening signpost "For each line of work, this section says where it places the hazard and what its comparisons hold fixed. §1 stated what ours holds fixed (Figure 2); how we searched is described at the end." (demo 02:5; the owner's at paper/finale.md:182-184) is cut, and the bold label "Where the hazard enters learning." is dropped (STYLE) |
| 3 | Table 1. Where the hazard enters the learning or planning problem. | framing | kept (demo 02:9) |
| 4 | work / agents and method / where the hazard enters | framing | kept (Table 1 header, demo 02:11) |
| 5 | Haksar & Schwager (2018) / aerial agents fighting wildfire; multi-agent deep Q-network / the task: a reward for moving to burning trees on the fire's boundary (their Algorithm 2); the paper gives the fire no way to harm the agents | haksar2018; paper/related_work_verification.md:940 | kept (demo 02:13); read in full (READS RULING) |
| 6 | JaxWildfire (Çakır et al., 2025) / one air-tanker agent; JAX cellular-automaton wildfire simulator / the reward, hazard-priced: a per-step penalty proportional to the number of burning cells, with a bonus for full extinction; harm to the agent is not described | cakir2025jaxwildfire; paper/related_work_verification.md:941 | kept (demo 02:14) |
| 7 | safe reinforcement learning, as García & Fernández (2015) define it / learning policies that maximize return while ensuring reasonable system performance and/or respecting safety constraints / a constraint or a cost, typically | garcia2015safe; paper/related_work_verification.md:957-961 | kept (demo 02:15) |
| 8 | VULCAN (Liu & Yan, 2026) / a proposed approach to multi-robot fire search and rescue, planned by a vision-language model rather than learned / a hazard cost map that folds in smoke, heat and sensing uncertainty | liu2026vulcan; paper/related_work_verification.md:942, :96-104 | kept (demo 02:16) |
| 9 | CHE (this paper) / 12 agents; independent PPO / ambient: the transition and observation kernels only; no reward, cost or constraint reads the fire, and the reward prices each death at $d_p = 0.5$, whatever its cause | ENV-6; ENV-1; docs/theory_foundations.md:85-100 | kept (demo 02:17) |
| 10 | CHE's reward is hazard-blind, while JaxWildfire's is hazard-priced: ours prices an outcome, each death the same (Definition 2 in §3.3). | decision log, DEF. 2 WORDING RULING (docs/decision_log.md:5287); ENV-1; cakir2025jaxwildfire; paper/related_work_verification.md:941 | edited: the demo's "CHE's reward is hazard-blind rather than hazard-priced (Definition 2): it prices an outcome, each death the same." (demo 02:19) now names the hazard-priced neighbour from Table 1 and points to the home, §3.3 (STRUCTURE.md §7) |
| 11 | VULCAN's preliminary evaluation covers baselines only, and its evaluation metric, cumulative hazard exposure, is also abbreviated CHE, unrelated to our environment's name. | liu2026vulcan; paper/related_work_verification.md:942 | edited, from owner text (paper/finale.md:201-204): the demo's "VULCAN's preliminary evaluation covers baselines, not the approach itself, and its evaluation metric is also abbreviated CHE (cumulative hazard exposure), which is unrelated to our environment's name." (P3 §6: a contrast closer; LEN) |
| 12 | Coupling A lets structural collapse add ignitions. | CLAUDE.md:18; docs/theory_foundations.md:286 | kept, from owner text (paper/finale.md:207-208); the bold label "A hazard that feeds on itself." is dropped (STYLE) |
| 13 | The nearest neighbour we found is Raut et al. (2026), who model public-safety power shutoffs as a single-agent decision problem. | raut2026psps; paper/related_work_verification.md:943, :526-540 | from owner text (paper/finale.md:208-210), split at the colon (40-word limit) |
| 14 | In it, the power flows that follow from the operator's switching decisions set the failure probability of lines in wildfire areas, which the authors treat as ignition risk. | raut2026psps; paper/related_work_verification.md:943 | from owner text (paper/finale.md:210-213) |
| 15 | Their reward is negative operating cost, and there is no spatial spread model. | raut2026psps; paper/related_work_verification.md:943, :532-540 | from owner text (paper/finale.md:213-214) |
| 16 | CHE's agents influence the hazard too, but weakly and indirectly: an agent standing on a weak cell raises that cell's collapse rate, yet most collapses happen with no agent present (§5.1). | CA-8; CA-9 | edited (class A, OI-4): the owner's "An agent standing on a weak cell raises that cell's collapse rate nine-fold (Definition 5), but most collapses happen with no agent present: under trained policies, agents add about one percent to the number of collapses per episode, and about seven percent under random policies." (paper/finale.md:214-218) and the demo's "an occupied weak cell collapses nine times as often per step as an empty one (Definition 5), yet agent load adds only 0.4–1.4 % to the collapses per episode under the trained policies of §5, and 7.4–8.3 % under random policies" (demo 02:21). The numbers move to their one home, §5.1 (STRUCTURE.md §7); "about seven percent" is gone. Departs from READS RULING item 2 ("Left as written, by the owner's call", docs/decision_log.md:5760-5765): class C pending transcription (Q4a) |
| 17 | A collapse may then seed fire, so we do not claim that CHE's hazard grows without agent influence. | docs/theory_foundations.md:286; CA-8 | from owner text (paper/finale.md:218-220) |
| 18 | The difference from Raut et al. is one of directness and size: there the controlled decision sets the failure probability, while in CHE ignition is not an action available to the agents. | raut2026psps; paper/related_work_verification.md:943 | from owner text (paper/finale.md:220-222); the clause "and where they stand moves the collapse count only slightly" is cut (it restates row 16; LEN) |
| 19 | Coupling B attenuates each agent's observation by Beer–Lambert transmittance along the line of sight through smoke. | docs/theory_foundations.md:344 | from owner text (paper/finale.md:225-226); the bold label "Perception degraded by the hazard." is dropped (STYLE) |
| 20 | VULCAN degrades simulated sensing with smoke density and visibility loss, and infers smoke density from image degradation and depth consistency, but it has no transmittance model. | liu2026vulcan; paper/related_work_verification.md:942 | from owner text (paper/finale.md:227-229) |
| 21 | JaxWildfire's observations are partial and egocentric but not attenuated. | cakir2025jaxwildfire; paper/related_work_verification.md:941 | from owner text (paper/finale.md:229-230) |
| 22 | In the search described below, we found no reinforcement-learning environment whose observation kernel attenuates by transmittance. | paper/related_work_verification.md:883-887, :912-917; DX-101 | from owner text (paper/finale.md:230-232); the demo's "as Coupling B does along each line of sight through smoke" is cut (row 19 says it) |
| 23 | CHE follows JaxMARL's environment conventions and trains with independent PPO. | rutherford2024jaxmarl; paper/related_work_verification.md:372; dewitt2020ippo; paper/related_work_verification.md:472; ENV-11 | kept (demo 02:25); the bold label "Simulators and benchmarks in JAX." is dropped (STYLE) |
| 24 | None of the JAX multi-agent benchmarks we surveyed, JaxMARL, Multi-Agent Craftax and Assistax, has an evolving, spreading lethal hazard field or perception attenuated by a hazard. | rutherford2024jaxmarl; alomari2025macraftax; hinckeldey2025assistax; paper/related_work_verification.md:944-945 | kept (demo 02:25) |
| 25 | Multi-Agent Craftax comes closest in kind: its agents lose health to hunger and enemies and can die, but its lava is static terrain that agents cannot enter. | alomari2025macraftax; paper/related_work_verification.md:944 | kept (demo 02:25) |
| 26 | In Crafter and in Craftax-Classic, the JAX reimplementation described alongside Craftax, lava is lethal, and Crafter and Craftax reward each health point regained and penalize each one lost, pricing an outcome, as our reward does. | hafner2022crafter; matthews2024craftax; paper/related_work_verification.md:947, :991-1000, :1010-1016 | edited: the demo's "pricing an outcome rather than the hazard, much as our reward prices each death" (P3 §6: a contrast closer) |
| 27 | POBAX is a single-agent suite for partial observability, and BenchMARL a multi-agent benchmarking library built on TorchRL. | tao2025pobax; bettini2024benchmarl; paper/related_work_verification.md:946, :418, :434 | edited: "built on TorchRL rather than JAX" becomes "built on TorchRL"; the demo's next sentence "and JaxWildfire has a spreading fire in JAX, with one agent" is cut (Table 1 says it; LEN) |
| 28 | Domain randomization trains on a broad, fixed distribution over simulator parameters so that the deployed setting looks like one more sample. | tobin2017dr; muratore2022drreview; paper/related_work_verification.md:600-601 | kept (demo 02:27); the bold label "Choosing a training distribution." is dropped (STYLE) |
| 29 | Unsupervised environment design adapts the distribution to the learner instead. | paper/related_work_verification.md:596-599 | kept (split from the next sentence) |
| 30 | PAIRED generates environments from a regret objective; Prioritized Level Replay revisits levels by their estimated learning potential and was later recast as environment design; and ACCEL evolves levels near the frontier of the agent's ability. | dennis2020paired; jiang2021plr; jiang2021robustplr; parkerholder2022accel; paper/related_work_verification.md:596-599 | kept (punctuation only) |
| 31 | These methods ask which distribution to train on, usually adaptively; we compare two fixed distributions and evaluate no adaptive curriculum (§10). | decision log, READS RULING item 4 (docs/decision_log.md:5770-5772) | kept (demo 02:27). The demo's next sentence, "Our held-out test belongs to the broader problem of zero-shot generalization <kirk2023zsg>.", is cut: §1 states it with the same citation (one home; LEN) |
| 32 | The closest earlier study of our question is Gao et al. (2024). | gao2024composition; paper/related_work_verification.md:613-626, :891-897 | kept (demo 02:29); the bold label "Compositional generalization over environmental factors." is dropped (STYLE) |
| 33 | In visual imitation learning for robotic manipulation, they ask whether policies compose environmental factors, such as object type and position, table texture and height, and camera position, to succeed on unseen combinations. | gao2024composition; paper/related_work_verification.md:948; decision log, §1 INTRODUCTION item 2 (docs/decision_log.md:5704-5713) | edited: "and use the answer to design data collection" is cut (LEN) |
| 34 | They compare data-collection strategies at a matched number of demonstrations, among them varying one factor at a time and cycling through factors so that more combinations appear (their §III-C and §IV-A). | gao2024composition; paper/related_work_verification.md:948, :617-622 | edited (class A, LEN: Gao to about three sentences): the demo's "They compare strategies, among them one that varies a single factor at a time from a base setting and one that cycles through factors so that more combinations appear, at a matched number of demonstrations and across levels of a rough effort proxy, the number of factor changes (their §III-C and §IV-A)."; the effort-proxy clause is cut |
| 35 | Policies do compose, more weakly when both factors are physical (their §V-B), and the strategy that covers more combinations does better. | gao2024composition; paper/related_work_verification.md:948 | kept (demo 02:29; paper/finale.md:281-283) |
| 36 | Their design is built for data efficiency and does not separate co-occurrence from how often each factor value appears; ours matches compute and, in the ISO-4 correction, the active share (§1). | gao2024composition; paper/related_work_verification.md:948, :617-622; DES-14 | edited: the demo's "Their design is built for data efficiency, not to separate co-occurrence from how often each factor value appears; ours matches compute and, in the ISO-4 correction, the share of training that carries any stressor." (P3 §6: a contrast closer; "active share" is §1's defined term). The demo's next sentence, "The settings differ too: their factors change what the robot sees and must do, and their policies are learned by imitation, while two of our stressors are causally coupled to a lethal hazard and our policies are learned by multi-agent reinforcement learning.", is cut (LEN) |
| 37 | CompoSuite studies the composition of tasks, over robots, objects, objectives and obstacles, in multi-task reinforcement learning. | mendez2022composuite; paper/related_work_verification.md:642-644 | edited: the demo's "CompoSuite studies compositional multi-task reinforcement learning over robots, objects, objectives and obstacles: composition of tasks, not of co-occurring stressors." (P3 §6: a contrast closer) |
| 38 | The DBCA method builds splits whose atom distributions are similar and whose compound distributions differ. | keysers2020; paper/related_work_verification.md:234 | kept (demo 02:29) |
| 39 | Our secondary sweep follows that idea, holding each coupling's frequency fixed while co-occurrence varies; our ISO and JOINT endpoints do not, since JOINT sees each coupling three times as often as ISO (§1, §9.1). | keysers2020; DES-7; decision log, ENDPOINT CONFOUND (docs/decision_log.md:4549-4570) | kept; "(§1, §9)" becomes "(§1, §9.1)", the confound's home |
| 40 | Robust reinforcement learning asks the same question about perturbations. | framing | kept (demo 02:31); the bold label "Mixed and simultaneous perturbations." is dropped (STYLE) |
| 41 | Erdem & Üre (2025) train single-agent continuous-control policies against a learned adversary that perturbs observations, actions, or both, and report that agents trained against one modality remain vulnerable to simultaneous attacks on both (their Tables 3–4). | erdem2025mixed; paper/related_work_verification.md:949, :1036-1038 | edited: two demo sentences merged; the demo's "at every step (their §3.4 and Algorithm 1)" moves to row 43 in the form the record supports |
| 42 | Under single-type attacks, agents trained against their balanced mixed adversary do at least as well as those trained against a naive one in all six cells, one a tie (their Table 5). | erdem2025mixed; paper/related_work_verification.md:1039-1041 | edited (class B, finding N15): the demo's and the owner's "agents trained against their balanced mixed adversary do better under single-type attacks than those trained against a naive mixed adversary (their Table 5)" (demo 02:31; paper/finale.md:305-307). The record says ASA-PPO ≥ N-HYBRID-PPO in 6 of 6 cells, one tie. Departs from text READS RULING item 2 recorded as final (docs/decision_log.md:5757-5765): class C pending transcription (Q4a) |
| 43 | Of their six training arms, one is an unattacked baseline, and in each of the others an attack is computed at every step, with no scheduled clean steps (their Algorithm 1). | erdem2025mixed; paper/related_work_verification.md:1042-1045; decision log, READS RULING item 2 (docs/decision_log.md:5760-5762) | edited (class A, OI-3): replaces the owner's "Because every arm is perturbed throughout," (paper/finale.md:310-311) and the demo's "Every adversarially trained arm is perturbed throughout" (demo 02:31) with what the full read records (six arms, one unattacked; the attack computed at every step, no scheduled clean steps). Departs from READS RULING item 2 ("Left as written, by the owner's call", docs/decision_log.md:5760-5765): class C pending transcription (Q4a) |
| 44 | No arm has a counterpart of the fire-only share our correction removes. | erdem2025mixed; paper/related_work_verification.md:1042-1045; DES-8 | from owner text (paper/finale.md:310-312: "their design has no counterpart of the fire-only share our correction removes"), now resting on row 43's premise (class A, OI-3; Q4a) |
| 45 | No arm trains on a mixture of single-type attacks, and the mixed arms carry the combined budget, which the authors note is more severe. | erdem2025mixed; paper/related_work_verification.md:949, :1042-1043 | from owner text (paper/finale.md:307-310); the clause "each single-type arm never meets the other modality" is cut (LEN) |
| 46 | Their design thus bundles per-modality frequency, co-occurrence and a larger budget, which is nearer to what our corrected contrast leaves in, where JOINT still sees each coupling twice as often as ISO-4; it neither supports nor contradicts our corrected null. | DES-14; RES-6; erdem2025mixed; paper/related_work_verification.md:1036-1045 | edited (class A, LEN), from owner text: the owner's "What it bundles is how much each arm sees of each modality, whether it sees them together, and a larger budget. That is nearer to what our corrected contrast leaves in, where JOINT still sees each coupling twice as often as ISO-4, though unlike ISO-4 their single-type arms see the other modality not at all. Their result is therefore not a test at matched per-modality exposure, and it neither supports nor contradicts our corrected null." (paper/finale.md:312-318), shortened |
| 47 | Agrawal et al. (2023) train multi-agent policies against random reward, state and action noise, one or two types at a time, under a curriculum that raises the noise level and sets training length, so exposure differs between their models. | agrawal2023multimodal; paper/related_work_verification.md:950, :151-155 | kept (demo 02:31); "noise types" becomes "types", "with a curriculum" becomes "under a curriculum" |
| 48 | In supervised vision, Tramèr & Boneh (2019) and Hsiung et al. (2023) study robustness to multiple and to composite perturbations. | tramer2019multiple; hsiung2023compositional; paper/related_work_verification.md:634-641 | kept (demo 02:31) |
| 49 | Chen et al. (2022) model domain randomization as returning the optimal history-dependent policy of a latent MDP, a set of fully observed MDPs that differ in their transitions. | chen2022understandingdr; paper/related_work_verification.md:952, :1046-1049 | kept (demo 02:33), split; the bold label "Theory." is dropped (STYLE) |
| 50 | Every upper bound they prove on its shortfall assumes each MDP is communicating, with bounded diameter. | chen2022understandingdr; paper/related_work_verification.md:1046-1048 | kept (demo 02:33) |
| 51 | Theorem 1 (§6) is kin to the construction of their Proposition 1, in which an irreversible choice is made before anything distinguishes the candidate MDPs. | chen2022understandingdr; paper/related_work_verification.md:952 | edited (class A, LEN: the Chen et al. paragraph shortened): replaces the demo's "Without that assumption, their Proposition 1 shows the shortfall can grow linearly in the horizon, through an irreversible choice made before anything distinguishes the candidate MDPs. Theorem 1 here (§6) is kin to that construction but not covered by it. Its no-information endpoint has the structure of their Proposition 1's uninformed commitment, with two branches." |
| 52 | Read as a latent MDP with the signals encoded as states, Theorem 1's two-corridor toy has an absorbing failure, so their upper bounds do not apply. | chen2022understandingdr; paper/related_work_verification.md:1049-1053 | edited (class A, LEN): the demo's "But its two-corridor toy, with the signals encoded as states, has an absorbing failure, so their diameter assumption fails and their upper bounds do not apply; it has a single terminal reward and can reveal the environment before the branch, which their Proposition 1 does not address;"; the terminal-reward clause is cut |
| 53 | It also measures a different gap, the adaptive optimum against the policy optimal for a fixed map. Chen et al. therefore do not subsume Theorem 1, and Theorem 1 does not extend their bounds. | chen2022understandingdr; paper/related_work_verification.md:952, :1049-1053 | kept (demo 02:33; paper/finale.md:341-346). The checker reads these two sentences as one unit ("map." ends in its "p." abbreviation) |
| 54 | Pynadath & Tambe (2002) relate the complexity of team decision problems with communication to observability. | pynadath2002; paper/related_work_verification.md:953 | kept (demo 02:33), split at the colon |
| 55 | Free communication lowers the complexity when the world is collectively observable (their Theorem 4 and Table 2), and makes no difference when it is individually observable or not observable at all (their Theorems 5–6). | pynadath2002; paper/related_work_verification.md:953; decision log, READS RULING item 4 (docs/decision_log.md:5771-5772) | kept (demo 02:33). Theorem 3 (NEXP to PSPACE under collective partial observability, recorded at :953) is not added (Q23, P3-N12) |
| 56 | Remark 2′ (§7) refines this for collective partial observability: communication's marginal value vanishes when interchangeable agents' views are redundant, and returns when roles are irreplaceable or deaths are costly. | pynadath2002; decision log, READS RULING item 4 (docs/decision_log.md:5771-5772); docs/theory_foundations.md:457 | kept (demo 02:33) |
| 57 | A survey of adaptability in multi-agent reinforcement learning (Hu et al., 2025, revised 2026) calls an environment family highly diagnostic if it "systematically varies" factors such as population, observability or communication structure "while holding other factors fixed". | hu2025adaptablemarl; paper/related_work_verification.md:951 | edited: the demo's "The survey by Hu et al. (2025, revised 2026) of adaptability in multi-agent reinforcement learning calls …" reordered; the quotation unchanged |
| 58 | It mentions compositional generalization but does not analyse shifts in several factors at once. | hu2025adaptablemarl; paper/related_work_verification.md:951 | kept (demo 02:33), as its own sentence |
| 59 | We ran the literature search with the help of LLM-based research assistants, between August and October 2026. | DX-101 | from owner text (paper/finale.md:362-363); the demo's "We searched with LLM-based research assistants between August and October 2026: first a census …" (demo 02:35) is replaced by the owner's wording, which DX-101 records as final |
| 60 | A census of benchmark venues and a search for theorems that could subsume ours came first; a search of domain randomization, environment design, multi-task and robust-learning neighbours followed. | DX-101; decision log, NO-SCOOP CHECKS (docs/decision_log.md:3334) | from owner text (paper/finale.md:363-366) |
| 61 | Both used web search and the arXiv API and read abstracts. | paper/related_work_verification.md:883-887 | from owner text (paper/finale.md:366) |
| 62 | The works this section describes in detail were then read in full; the remaining citations rest on their abstracts. | paper/related_work_verification.md:928-937; decision log, READS RULING (docs/decision_log.md:5737-5753) | from owner text (paper/finale.md:367-368) |
| 63 | We did not query IEEE Xplore. | paper/related_work_verification.md:886; decision log, READS RULING item 5 (docs/decision_log.md:5775-5776) | from owner text (paper/finale.md:368) |
| 64 | Wherever this paper says that no work does something, it means no work found by this search. | framing | from owner text (paper/finale.md:369-370) |

## Findings

New findings of the fix-list kinds, made while writing. Not applied.

- **correctness of a carried framing, class C (report only).** The demo's
  and the owner's paragraph label "A hazard that feeds on itself"
  (demo 02:21; `paper/finale.md:207`) is not literally true of Coupling A:
  collapse seeds fire, but the structure kernel `T_C(c, x)` reads no hazard
  state (`CLAUDE.md` invariant #2, `docs/theory_foundations.md:286`), so the
  label may read as the fire causing collapse. The label is dropped here for style (bold
  run-ins), not as a correction. Direction: if the owner restores a label,
  "Collapse that feeds the fire".

## Cut from the demo (for the owner's revert)

Each is quoted in the change column of the row it was cut from (rows 2,
18, 22, 27, 31, 33, 34, 36, 37, 45, 46, 51, 52). No characterization of a cited work was
added; every cut removes detail the record supports.

## Alternates

None for this section (`STRUCTURE.md` §9 names none).

## Open items

1. **Q4a, class C pending transcription (RV-R1).** Three sentences change
   text that READS RULING item 2 recorded as "Left as written, by the
   owner's call" (`docs/decision_log.md:5760-5765`), and no transcribed
   ruling supersedes it yet:
   - row 43 (OI-3), the owner's "every arm is perturbed throughout"
     (`paper/finale.md:310-311`; the demo: "Every adversarially trained arm
     is perturbed throughout"), now "one is an unattacked baseline, and in
     each of the others an attack is computed at every step, with no
     scheduled clean steps (their Algorithm 1)" (RWV :1042-1045);
   - row 16 (OI-4), the owner's "agents add about one percent … and about
     seven percent under random policies" (`paper/finale.md:217-218`), now a
     pointer to §5.1, where W4 states CA-9's range with its scope (7.4–8.3 %
     as an increase under random policies; 0.4–1.4 % under the trained
     Phase-3 policies);
   - row 42 (N15, class B), the owner's "also do better under single-type
     attacks" (`paper/finale.md:305-307`), now "do at least as well … in all
     six cells, one a tie" (RWV :1039-1041).
   Revert: each row's change column quotes the owner's wording. A one-line
   transcribed ruling superseding READS RULING item 2 for v2 would settle
   all three.
2. **The pointer in row 16 depends on W4's §5.1.** In the last build of
   this session it resolves to "5.1 Definition and implementation", and
   W4's paragraph there states CA-8 and CA-9 with the trained-policy scope
   (`sections/05_coupling_a.md:44`, as read this session). If §5.1 changes,
   this pointer must follow; §2 states no agent-influence number by design.
3. **Cross-references to Theorem 1 (§6) and Remark 2′ (§7)** (rows 51–53,
   56) resolve in the last build of this session to W4's statements.
4. **Q23 (P3-N12), not added.** Pynadath & Tambe's Theorem 3 (NEXP to
   PSPACE under collective partial observability, RWV :953) stays out unless
   the owner approves it.
5. **Budget (Q20).** 1,270 prose words, 10 % over 1,150, at the edge of the
   ±10 % band. Further cuts, owner's choice: row 26's Crafter/Craftax
   sentence (35 words) or row 47's Agrawal et al. sentence (37 words), whose
   point (exposure differs between their models) Erdem & Üre's paragraph
   already makes for its closer neighbour.
6. **Nothing unsourced.** Five tags (ENV-6 and ENV-1 in Table 1; DES-7,
   DES-14 and DX-101 in prose), all resolving; no new ledger row was
   needed.
