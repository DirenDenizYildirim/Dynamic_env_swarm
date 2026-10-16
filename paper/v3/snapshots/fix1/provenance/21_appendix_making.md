# Provenance: sections/21_appendix_making.md

Writer: W5 (Paper v3, step 4.1, 2026-10-14). Checked with
`paper/v3/src/provenance_check.py --strict`. App. I is the owner's search
paragraph from v2 §2 (`paper/finale.md:362-370`), moved. **App. J is a
builder draft for the owner to edit (OWNER-EDITS; PAPER V3 item 6,
log:6193-6202).** It starts from the builder recommendation the ruling
quotes; it does not draft the `<d-footnote>`, which is the owner's alone, and it
does not assert that the ideas are human-sourced (the owner's statement to
make, STUB-SPEC). Carried v2 A1 (footnote scope; attribution; rewriting) stays
open: `<!-- OWNER-PENDING:A1 -->`.

| # | sentence (verbatim) | support | change from v2, and why |
|---|---|---|---|
| 1 | I How the literature search ran | framing | new heading (STRUCTURE §2: the search moves from v2 §2 to App. I) |
| 2 | We ran the literature search with the help of LLM-based research assistants, between August and October 2026. | DX-101 | kept: owner text (paper/finale.md:362-363) as v2 §2 carried it (paper/v2/sections/02_related_work.md:49) |
| 3 | A census of benchmark venues and a search for theorems that could subsume ours came first; a search of domain randomization, environment design, multi-task and robust-learning neighbours followed. | DX-101; decision log, NO-SCOOP CHECKS (docs/decision_log.md:3334) | kept: owner text (paper/finale.md:363-366) |
| 4 | Both used web search and the arXiv API and read abstracts. | paper/related_work_verification.md:883-887 | kept: owner text (paper/finale.md:366) |
| 5 | The works §2 describes in detail were then read in full; the remaining citations rest on their abstracts. | paper/related_work_verification.md:928-937; decision log, READS RULING (docs/decision_log.md:5737-5753) | edited: owner text (paper/finale.md:367-368) with "this section" → "§2" (the paragraph moved to the appendix) |
| 6 | We did not query IEEE Xplore. | paper/related_work_verification.md:886; decision log, READS RULING item 5 (docs/decision_log.md:5775-5776) | kept: owner text (paper/finale.md:368) |
| 7 | Wherever this paper says that no work does something, it means no work found by this search. | framing | kept: owner text (paper/finale.md:369-370) |
| 8 | J How this paper was made | framing; decision log, PAPER V3 (docs/decision_log.md:6197-6202, item 6: the appendix "How this paper was made") | new (OWNER-EDITS) |
| 9 | This study was carried out by its authors with an LLM assistant, Claude (Anthropic), used through Claude Code. | decision log, SCAFFOLDING SITE (docs/decision_log.md:5364, a Claude Code web session); decision log, PAPER V2 (docs/decision_log.md:6047-6052, builder subagents); CLAUDE.md:3 | new (OWNER-EDITS). Names the tool, not the author (BRIEF §11). The tool's exact naming is the owner's (carried A1) |
| 10 | The authors made or ratified the study's decisions, among them the environment's design, the constants fixed before the main experiment, the scope of the post hoc interaction check, the reading of the results and the framing of this paper. | decision log, PAPER V2 (docs/decision_log.md:6047-6050), item 1; decision log, PAPER V3 PHASE 1 START (docs/decision_log.md:6226-6235, the check's scope); decision log, PRE-RENTAL DELEGATION AND RATIFICATIONS (docs/decision_log.md:3104-3112) | edited (OWNER-EDITS); fix round RC2-2 (MUST): "made the study's decisions" → "made or ratified"; "the registered design and its amendments" and "the plan of the post hoc interaction check" removed from the list, since the record shows delegation and no transcribed approval |
| 11 | Some decisions are recorded as delegated to the assistant: the authors delegated the design decisions taken before the main training runs, including the ratification of the registered outcome framings, giving the avoidance of their own bias as the reason, and a few later rulings were the assistant's call at the authors' request. | decision log, PRE-RENTAL DELEGATION AND RATIFICATIONS (docs/decision_log.md:3104-3112: "the decisions are yours this time and I am making it to save potential bias now"); phase6_framing_branches.md:3-4 (ratified in that entry); decision log, GRID CHUNKING (docs/decision_log.md:3450, "owner-requested, builder-ruled"); decision log, OPENING AND §1 REOPENED (docs/decision_log.md:5961, "owner delegated, builder's call") | new (OWNER-EDITS); fix round RC2-2 |
| 12 | From early in the project, a decision bound only once it was written into the project's dated decision record; before that rule, some directives existed only in conversation. | decision log, Phase-5 pre-flight rulings, round 2 (docs/decision_log.md:423, :465-468: the transcription meta-rule, 2026-07-28); docs/decision_log.md:455-460 (a rule cited as binding that existed only in conversation); CLAUDE.md:273-276 | edited (OWNER-EDITS); fix round RC2-2: replaces "Each decision was written into the project's dated decision record before it was acted on", which the rule's 2026-07-28 start contradicts |
| 13 | The analysis plan of the post hoc interaction check was written by the assistant, and no approval of it by the authors is yet recorded. | che/bench/results/phase6/post_v3_interaction/PLAN.md:3 (written 2026-10-14 by the builder before any run); docs/decision_log.md:6218-6244 (the log's last entry; no approval of PLAN.md transcribed) | new (OWNER-EDITS); fix round RC2-2. OWNER-PENDING:PLAN_OK: if the owner's OK is transcribed, this sentence changes |
| 14 | The assistant implemented the code and tests to these decisions, ran analyses on the authors' instruction, drafted reports, figures and reviews of the design, proposed options for the authors to accept or reject, and drafted this paper's text section by section. | CLAUDE.md:3; decision log, WRITING ROLES (docs/decision_log.md:5429); decision log, PAPER V2 (docs/decision_log.md:6036), item 1 and the process amendment; decision log, PAPER V3 (docs/decision_log.md:6197-6202) | edited (OWNER-EDITS); fix round RC2-2 ("those" → "these") |
| 15 | Some proposals came from the assistant. | decision log, PAPER V3 (docs/decision_log.md:6197-6200, item 6: "some proposals came from the assistant") | new (OWNER-EDITS), the builder's recommendation as the ruling quotes it |
| 16 | In particular, the inert-share bias in the isolated arm and the correcting arm ISO-4 were first raised in an assistant-drafted review of the registered design, and the authors adopted both and registered them before unblinding (Appendix D). | decision log, PAPER V3 (docs/decision_log.md:6199-6201: "the inert-share bias and ISO‑4 were first raised in an assistant-drafted review and adopted by the owner"); docs/venue_review_2026-08-16.md:1; DES-15 | new (OWNER-EDITS). The attribution is carried v2 A1(ii), OWNER-PENDING; App. D (W4) says only "a review of the registered design" by default |
| 17 | Every sentence of this paper has a provenance record that ties it to a decision, a row of the numbers ledger or a committed file, and every number in the text comes from that ledger, whose rows cite the file and line they were read from or show their derivation. | paper_v3_prompt.md:57-58 ("Every sentence gets a provenance row"); paper_v3_prompt.md:113-117 (numbers only from the ledgers, VERIFIED or DERIVED) | new (OWNER-EDITS) |
| 18 | Separate assistant instances reviewed the drafts. | decision log, PAPER V2 (docs/decision_log.md:6096-6107, the process amendment: reviewer agents, a blind agent) | new (OWNER-EDITS) |
| 19 | The authors checked every word and are responsible for the whole. | decision log, PAPER V2 (docs/decision_log.md:6047-6050, item 1: "The owner checks every word ... and is responsible for the result") | new (OWNER-EDITS). A statement the owner makes; true only once the owner's check is done (step 4.5) |

## Findings

- Word count: I 103 prose words (about 150 budgeted); J about 220 (about 250).
- App. J names the tool as "Claude (Anthropic), used through Claude Code".
  The record names Claude Code for the scaffolding site (log:5364) and
  "Claude's web-verification agents" (log:5745); the literature search used
  "LLM-based research assistants" (owner text). Whether one name covers
  every tool used is the owner's to confirm.
