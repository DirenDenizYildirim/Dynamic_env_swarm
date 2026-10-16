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
| 10 | The authors made the study's decisions: the environment's design, the constants fixed before the main experiment, the registered design and its amendments, the plan of the post hoc interaction check, the reading of each result and the framing of this paper. | decision log, PAPER V2 (docs/decision_log.md:6036), item 1; CLAUDE.md:273-276 (rulings bind once transcribed); docs/decision_log.md:6226-6235 (the interaction-check scope ruled by the owner) | new (OWNER-EDITS), from PAPER V3 item 6's "states the division of labour" |
| 11 | Each decision was written into the project's dated decision record before it was acted on. | CLAUDE.md:273-279 ("A chat ruling binds only once it is transcribed into decision_log.md or CLAUDE.md in the same session") | new (OWNER-EDITS) |
| 12 | The assistant implemented the code and tests to those decisions, ran analyses on the authors' instruction, drafted reports, figures and reviews of the design, proposed options for the authors to accept or reject, and drafted this paper's text section by section. | CLAUDE.md:3 ("You are the implementation engineer"); decision log, WRITING ROLES (docs/decision_log.md:5429); decision log, PAPER V2 (docs/decision_log.md:6036), item 1 and the process amendment; decision log, PAPER V3 (docs/decision_log.md:6197-6202) | new (OWNER-EDITS) |
| 13 | Some proposals came from the assistant. | decision log, PAPER V3 (docs/decision_log.md:6197-6200, item 6: "some proposals came from the assistant") | new (OWNER-EDITS), the builder's recommendation as the ruling quotes it |
| 14 | In particular, the inert-share bias in the isolated arm and the correcting arm ISO-4 were first raised in an assistant-drafted review of the registered design, and the authors adopted both and registered them before unblinding (Appendix D). | decision log, PAPER V3 (docs/decision_log.md:6199-6201: "the inert-share bias and ISO‑4 were first raised in an assistant-drafted review and adopted by the owner"); docs/venue_review_2026-08-16.md:1; DES-15 | new (OWNER-EDITS). The attribution is carried v2 A1(ii), OWNER-PENDING; App. D (W4) says only "a review of the registered design" by default |
| 15 | Every sentence of this paper has a provenance record that ties it to a decision, a row of the numbers ledger or a committed file, and every number in the text comes from that ledger, whose rows cite the file and line they were read from or show their derivation. | paper_v3_prompt.md:57-58 ("Every sentence gets a provenance row"); paper_v3_prompt.md:113-117 (numbers only from the ledgers, VERIFIED or DERIVED) | new (OWNER-EDITS) |
| 16 | Separate assistant instances reviewed the drafts. | decision log, PAPER V2 (docs/decision_log.md:6096-6107, the process amendment: reviewer agents, a blind agent) | new (OWNER-EDITS) |
| 17 | The authors checked every word and are responsible for the whole. | decision log, PAPER V2 (docs/decision_log.md:6047-6050, item 1: "The owner checks every word ... and is responsible for the result") | new (OWNER-EDITS). A statement the owner makes; true only once the owner's check is done (step 4.5) |

## Findings

- Word count: I 103 prose words (about 150 budgeted); J about 220 (about 250).
- App. J names the tool as "Claude (Anthropic), used through Claude Code".
  The record names Claude Code for the scaffolding site (log:5364) and
  "Claude's web-verification agents" (log:5745); the literature search used
  "LLM-based research assistants" (owner text). Whether one name covers
  every tool used is the owner's to confirm.
