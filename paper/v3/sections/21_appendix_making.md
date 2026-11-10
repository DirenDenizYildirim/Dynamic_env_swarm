<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### H How the literature search ran

We ran the literature search with the help of LLM-based research assistants, between August and October 2026<!-- N:DX-101 -->. A census of benchmark venues and a search for theorems that could subsume ours came first; a search of domain randomization, environment design, multi-task and robust-learning neighbours followed. Both used web search and the arXiv API and read abstracts. The works §2 describes in detail were then read in full; the remaining citations rest on their abstracts. We did not query IEEE Xplore. Seven works in §2 and §4.4 (FireCommander, PyroRL, the recurrent-Q study, CARL, CompoSuite and two learned-communication methods) were added after an external review of a draft named them; we checked each against its published record. Wherever this paper says that no work does something, it means no work found by this search.

### I How this paper was made

<!-- OWNER-EDITS: the whole of Appendix I (lettered J until the interaction check's appendix was removed), from this heading to the end of the file, is a builder draft for the owner to edit (PAPER V3 item 6, docs/decision_log.md:6193-6202). The disclosure footnote on the abstract is the owner's alone and is not drafted here. -->
<!-- A1 settled 2026-11-03: the owner approved Appendix I and the footnote, confirmed reading and checking the whole paper, and takes full responsibility. -->
<!-- carried v2 A1: (i) the footnote's scope; (ii) attributing the review that first raised the inert-share bias and ISO-4 to the assistant (the draft below follows PAPER V3 item 6); (iii) whether the owner rewrites parts of the text -->

This study was carried out by its authors with an LLM assistant, Claude (Anthropic), used through Claude Code. We say here plainly who did what.

Claude wrote the simulator, that is, the environment's code and its tests, and the authors debugged it. The simulator's design was not left wholly to either side: the authors made some of its design decisions, and others were left to Claude.

Before the GPU runs, the authors also left to Claude the remaining decisions about the experiment, among them the seed layout, the run order, the branch rules and the ratification of the registered outcome framings; the authors gave avoiding their own bias as the reason. A few later rulings were also Claude's call, at the authors' request. From early in the project, a decision counted only once it was written into the project's dated decision record; before that rule, some directives existed only in conversation.

<!-- the interaction check's scope and plan sentences are removed (NO INTERACTION CHECK, 2026-10-19): the check is not run and the paper does not describe it -->

Claude also ran the analyses on the authors' instruction, drafted the reports and figures, drafted this paper's text section by section, and revised it after an external review of the draft. Some proposals came from Claude. In particular, it first raised the inert-share bias in the isolated arm and proposed the correcting arm ISO-4, in a review of the registered design; the authors adopted both and registered them before unblinding (Appendix D). Separate Claude instances reviewed the drafts.

Every sentence of this paper has a provenance record that ties it to a decision, a row of the numbers ledger or a committed file, and every number in the text comes from that ledger, whose rows cite the file and line they were read from or show their derivation, except the few added in the final revision after an external review, whose provenance records cite their source files directly. The authors read and checked the whole paper and take full responsibility for it.

<!-- END OWNER-EDITS (Appendix I) -->
