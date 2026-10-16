# Step 4.5: the blind review, run by the owner outside this repository

`paper_v3_prompt.md` step 4.5: the blind review runs in a **separate session
that you start outside this repository**, so that `CLAUDE.md` does not load
into the reviewer's context (it did in v2). Give it only the three files below
and the prompt at the end. If that is not possible, record that the review was
not fully blind.

## 1. The three files (copy them out of the repository first)

| file | what it is |
|---|---|
| `paper/v3/out/submission_v3_print.pdf` | the printed paper, from the real-kit build |
| `paper/v3/out/submission_folder.zip` | the staged Beyond PDF submission (comments stripped) |
| `paper/v3/out/che_supplement.zip` | the anonymized code supplement (not in git; rebuild it with `paper/v3/supplement/package.py` if missing) |

## 2. Where to run it

- **Best:** a new Claude conversation on claude.ai (not Claude Code), with the
  three files attached. No repository, so no `CLAUDE.md`.
- **Or:** Claude Code started in a new empty folder, containing only the three
  files, on a machine where that folder is not inside this repository. Check
  that no `CLAUDE.md` exists in the folder or any parent folder.
- **Not:** a session on this repository, or a cloud session with the
  repository attached.

## 3. The prompt to paste

> You are an anonymous reviewer for TMLR (Transactions on Machine Learning
> Research). The attached submission is a Beyond PDF article: the PDF is its
> printed form, the zip is the submitted Markdown/HTML folder, and the second
> zip is the anonymized code supplement. Review it as TMLR asks: are the claims
> supported by accurate, convincing and clear evidence, and would some
> individuals in TMLR's audience be interested in the findings?
>
> Use only the attached files. Do not search the web for the paper or its
> authors, and do not try to identify the authors.
>
> Write: (1) a summary of the submission in your own words; (2) strengths;
> (3) weaknesses, numbered, each with the page or section and the evidence;
> (4) whether the code supplement supports the claims it is said to support
> (you may unpack and run it; say what you ran); (5) every sentence you found
> unclear or garbled, quoted with its page; (6) requested changes; (7) a
> recommendation (accept, minor revision, major revision, reject) with your
> confidence from 1 to 5.

## 4. Afterwards

Save the review as `paper/v3/review/blind_review.md`, with one line saying where
it ran and whether it was fully blind. The next session reads it alongside the
open owner questions.
