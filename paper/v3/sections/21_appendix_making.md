<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### I How the literature search ran

<!-- STUB-SPEC
JOB: I: how the literature search ran (moved from §2). J: how this paper was made, starting from the builder's recommendation quoted in PAPER V3 item 6, for the owner to edit.
WRITER: W5.
BUDGET: I about 150 prose words; J about 250 prose words.
FROM: P1 §6.1 I and J; PAPER V3 item 6 (log:6193-6202); v2 §2 "How we searched".
ORDER:
  - I: the search procedure and its verification (DX-101), as v2 §2 described it; the novelty caveat ("in the search described here we found no …").
  - J (heading "### J How this paper was made", below): the division of labour (the authors made the rulings, checked every word and are responsible for it; an LLM assistant drafted text, code, analyses, figures, reviews and proposed options, as the record documents); that some proposals came from the assistant, in particular that the inert-share bias and ISO-4 were first raised in an assistant-drafted review and adopted by the authors; that every sentence has a provenance record. Name the tool, never the author. The owner edits this; carried v2 A1 (scope and attribution) stays open.
ROWS: DX-101.
REGISTERED STRINGS: none.
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
OWNER-PENDING:
  - the whole of J is the owner's to edit (PAPER V3 item 6); the footnote is the owner's alone.
  - carried v2 A1(i)–(iii).
NOT HERE: names, accounts, URLs, hashes; claims the record does not show (do not assert that the ideas are human-sourced; that is the owner's statement); the footnote text.
V2 MATERIAL: paper/v2/sections/02_related_work.md ("How we searched"); paper/v2/OWNER_QUESTIONS.md A1.
-->

We ran the literature search with the help of LLM-based research assistants, between August and October 2026<!-- N:DX-101 -->. A census of benchmark venues and a search for theorems that could subsume ours came first; a search of domain randomization, environment design, multi-task and robust-learning neighbours followed. Both used web search and the arXiv API and read abstracts. The works §2 describes in detail were then read in full; the remaining citations rest on their abstracts. We did not query IEEE Xplore. Wherever this paper says that no work does something, it means no work found by this search.

### J How this paper was made

<!-- OWNER-EDITS: the whole of Appendix J, from this heading to the end of the file, is a builder draft for the owner to edit (PAPER V3 item 6, docs/decision_log.md:6193-6202). The disclosure footnote on the abstract is the owner's alone and is not drafted here. -->
<!-- OWNER-PENDING:A1 -->
<!-- carried v2 A1: (i) the footnote's scope; (ii) attributing the review that first raised the inert-share bias and ISO-4 to the assistant (the draft below follows PAPER V3 item 6); (iii) whether the owner rewrites parts of the text -->

This study was carried out by its authors with an LLM assistant, Claude (Anthropic), used through Claude Code. The authors made or ratified the study's decisions, among them the environment's design, the constants fixed before the main experiment, the registered design, the scope of the post hoc interaction check, the reading of the results and the framing of this paper. Some decisions are recorded as delegated to the assistant: on the authors' instruction, the assistant made the remaining design decisions before the GPU rental, among them the seed layout, the run order, the branch rules and the ratification of the registered outcome framings, and the authors gave avoiding their own bias as the reason. A few later rulings were the assistant's call at the authors' request. From early in the project, a decision bound only once it was written into the project's dated decision record; before that rule, some directives existed only in conversation.

<!-- OWNER-PENDING:PLAN_OK no owner approval of PLAN.md is transcribed (log ends at the PAPER V3 PHASE 1 START entry); once the owner's OK is transcribed, replace the next sentence with "The authors approved that plan before the run" or similar -->

The analysis plan of the post hoc interaction check was written by the assistant, and no approval of it by the authors is yet recorded. The assistant implemented the code and tests to these decisions, ran analyses on the authors' instruction, drafted reports, figures and reviews of the design, proposed options for the authors to accept or reject, and drafted this paper's text section by section.

Some proposals came from the assistant. In particular, the inert-share bias in the isolated arm and the correcting arm ISO-4 were first raised in an assistant-drafted review of the registered design, and the authors adopted both and registered them before unblinding (Appendix D).

Every sentence of this paper has a provenance record that ties it to a decision, a row of the numbers ledger or a committed file, and every number in the text comes from that ledger, whose rows cite the file and line they were read from or show their derivation. Separate assistant instances reviewed the drafts. The authors checked every word and are responsible for the whole.

<!-- END OWNER-EDITS (Appendix J) -->
