# Provenance template (Paper v2; builder B2, 2026-10-11)

Copy this file to `provenance/NN_slug.md`, with the same name as the section
file (`sections/03_environment.md` → `provenance/03_environment.md`; an
alternate `sections/alt/00_abstract.no_recommendation.md` →
`provenance/00_abstract.no_recommendation.md`). Delete these instructions
in the copy and keep everything from "# Provenance:" down. Format:
`paper/v2/INTERFACE.md`, "Provenance rows". Checked by
`python paper/v2/src/provenance_check.py` (see `paper/v2/src/README.md`).

## Rules

1. **One row per sentence, in the section's order.** These count as
   sentences: every prose sentence; each heading; each list item's
   sentences; figure captions, including their "Status:" notes; `alt`,
   `caption` and iframe `title` text; the `<d-footnote>` text; listing
   labels ("**Listing 1.** …", which join the sentence after them); and
   table rows that carry a claim.
2. **The sentence column is the sentence as it stands in the section.**
   Copy it from the source or as plain text: the checker drops comments
   (ledger tags included), HTML tags, `<d-cite>` tags, `**`, `*` and
   backticks on both sides, and collapses spaces, before it compares.
   **Inline math is compared as written**, so copy `$\kappa_B = 0$`, not
   "κB = 0". Write a pipe inside a cell as `\|`.
3. **Table rows.** Either one row for the whole table row, its cells
   joined by ` / ` (for example `ISO / 0.63 / 0.71`), or one row per
   cell that carries a claim. Header rows count like any other row.
4. **Support** is one or more of, separated by `;`:
   - ledger ID(s): `RES-2; DES-13` (canonical ledger,
     `ledger_supplement.md` or `ledger_proposals/W<n>.md`);
   - a decision-log entry heading with its line:
     `decision log, PAPER V2 (docs/decision_log.md:6036)`;
   - file:line or file:start-end, repository-relative or a file name that
     is unique in the repository: `che/env/env.py:298-358`;
   - a citation key plus the `related_work_verification.md` line that
     supports the use: `garet2004chemical; paper/related_work_verification.md:1150`;
   - `framing`, for a sentence that makes no claim.
5. **Change column:** `kept`, `edited`, `new`, or `from owner text
   (paper/finale.md:<line>)`; then the fix-list item or finding and its
   class ("class A, F3"; "class B, finding N12"). For class B, quote the
   demo's or the owner's original wording, so the owner can revert.
6. **Only the table whose header reads `| # | sentence … |` is checked.**
   Other tables in the file (W1's title candidates and `description`) and
   the lists below are for the owner and are not compared with the section.
7. Keep the file in step with the section. After every edit, run the
   checker: a sentence with no row means an unsourced sentence, and a row
   with no sentence means a stale row.

---

# Provenance: sections/NN_slug.md

Writer: W<n>. Checked against the section on <date> (`snapshot.sh` label
`<label>`, if one was taken).

| # | sentence (verbatim) | support | change from the demo, and why |
|---|---|---|---|
| 1 | <heading text, e.g. "9 The pre-registered compositional test"> | framing | kept |
| 2 | <a sentence with a number, copied as it stands> | RES-2; DES-13 | edited: <what changed>; class A, F2 |
| 3 | <a sentence that cites a work> | garet2004chemical; paper/related_work_verification.md:<line> | new; class A, C1 |
| 4 | <a sentence that rests on a ruling> | decision log, <ENTRY HEADING> (docs/decision_log.md:<line>) | kept |
| 5 | <a sentence that rests on code> | che/env/structure.py:83-102 | kept |
| 6 | <a sentence that makes no claim> | framing | new |

## Findings

New findings of the fix-list kinds, made while writing (BRIEF.md): kind,
location, evidence, proposed direction. Not applied unless class B.

- <kind> `<location>`: <evidence>. Direction: <proposal>.

## Alternates

The `sections/alt/` variants written for owner choices, and which one this
section recommends.

- `sections/alt/<NN_slug>.<variant>.md`: <what differs>.
