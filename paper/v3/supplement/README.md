# Code supplement builder (Paper v3, step 2; V3-V1, V3-V3)

**For the orchestrator and the owner. Not shipped.** The file that ships as
the supplement's own README is `SHIPPED_README.md` (copied in as `README.md`).

Built 2026-10-14 under PAPER V3 items 1(5) and 2(e), and PAPER V3 PHASE 1
START. No git command that writes was run. Nothing outside
`paper/v3/supplement/` and `paper/v3/out/` was written. The source tree is
read only: every rewrite happens in a temporary staged copy.

## Files

| file | job |
|---|---|
| `package.py` | selects by rule → stages a copy → scrubs it → rebuilds `.manifest` entries → writes `README.md` + `SHA256SUMS` → writes a deterministic zip to `paper/v3/out/che_supplement.zip` |
| `rules.py` | the selection rules (`INCLUDE`), the scrub rules (`SCRUBS`), and what the scrub check forbids (`FORBIDDEN`, `WARN`) |
| `check_scrub.py` | (a) unpacks the zip; any identifying string is a FAIL |
| `check_size.py` | (b) zip size against TMLR's verified limit |
| `check_tests.py` | (c) unpack into a fresh directory, `uv sync --python 3.12 --group dev --locked`, then `pytest -q -rs che/tests` |
| `check_manifest.py` | (d) every file against `SHA256SUMS`, with no file missing or extra |
| `check_reproduce.py` | (e, extra) inside the unpacked supplement, re-runs the registered instruments and compares with the committed outputs |
| `run_checks.sh` | package, then all five checks: `bash paper/v3/supplement/run_checks.sh WORKDIR [package switches]` |
| `SHIPPED_README.md` | the neutral README that ships |

Outputs in `paper/v3/out/` (none of them ships):

- `che_supplement.zip`;
- `build_summary.json`;
- `selection_log.tsv`: every shipped file, with its rule;
- `excluded_summary.txt`;
- `scrub_log.tsv`: every rewrite, before and after. **It quotes the original
  identifying strings.**
- `package_console.txt` and `checks_summary.txt`.

**Re-run at phase end** (from the repository root; about 15–25 min on CPU):

    bash paper/v3/supplement/run_checks.sh <fresh scratch dir>

## Selection rules (what goes in, and why)

The base set is what git would track: `git ls-files --cached --others
--exclude-standard`. That covers tracked files, plus new files that
`.gitignore` does not exclude, so files added this session are picked up.
Symlinks never ship. A file ships if it matches the first rule below that
fits. No file over 20 MB ships. A **deny list** (`rules.DENY`) is checked
first. Today it holds one entry: `post_v3_interaction/RUNBOOK*`, the owner's
GPU runbook. It talks about "your laptop", the backup, and cloning "the
private repository". Without the deny entry it would ship under R1.

| rule | pattern | why |
|---|---|---|
| C1 | `che/**` except `che/bench/results/` | the package: env, train, eval, calibration, bench, configs, tests (incl. `tests/golden`), scripts. New `interaction_*` configs, scripts and tests land here automatically |
| C2 | `pyproject.toml`, `uv.lock` | install, with the exact lock |
| C3 | `LICENSE` | MIT; copyright holder → "Anonymous Authors" |
| D1 | `docs/locks.yaml` | three tests read it |
| D2 | `phase6_design_v2.md`, `phase6_framing_branches.md` | the registration documents (V3-V1) |
| D3 | `docs/theory_foundations.md` | **on by default** (`--no-theory`); see the recommendation below |
| D4 | `{severity,coupling_a,kappa_b,comms}_lock.md` | **on by default** (`--no-lock-records`): `locks.yaml` cites them as the ruling documents, and the ledger cites them as number sources |
| R5 | `phase6/post_v3_interaction*/**` except `*.tar.zst` | the post hoc interaction check, whatever the run returns (plan, evals, floors, report) |
| R1 | `che/bench/results/**/*.{md,txt,json,csv,sha256,yaml}` | every text result of every phase: reports, eval summaries, provenance, timings, floors, hash lists. These are the ledger's sources (11.3 MB raw) |
| R2 | `results/{phase1-5,e1,m05,m06}/**/*.npz` | small calibration arrays, e.g. `calibration_crossing.npz` and `estimates.npz` (4.3 MB) |
| R3 | `phase6/{g1_conf_5090,g1_iso4_5090,g1_t2000_5090}/eval_*.npz` | per-episode eval arrays for ISO/JOINT (k = 72), ISO-4 (k = 20) and T = 2000 (7.9 MB) |
| R4 | `phase6/{g1_sec_s1_12_5090,g1_t2000_5090}/*.jsonl` and `phase6/g1_grid/{sweep,ident}_*_s13..20.jsonl` | the 168 training logs the registered instruments read (187 MB raw, about 27 MB zipped). Found by tracing every file the four instrument runs open (an audit hook on `open`) |
| R6 | `phase6/g1_conf_5090/{iso,joint}_s*.jsonl` | **off by default** (`--conf-logs`): learning curves of the confirmatory arms. No registered instrument reads them. They add about 23 MB zipped, and fit if the owner wants them |
| decision log | `--decision-log-section REGEX` (repeatable) | **off by default. Owner decision**, because the entries quote the owner. Matching `## ` sections ship verbatim (scrubbed) as `docs/decision_log_excerpts.md` |

**Generated in the staged copy:**

- `README.md`;
- `SHA256SUMS`;
- `.manifest/<tag>.done`, plus a `.manifest/RECONSTRUCTED.txt` note, in each
  result directory that ships eval JSONs and a `SHA256_CKPT.txt`. 635 entries
  in 11 directories. This is on by default; `--no-manifests` turns it off.

### What is left out, and why (`excluded_summary.txt`)

| left out | files | raw size | why |
|---|---|---|---|
| other `.jsonl` training/bench logs | 595 | 505 MB | no paper-number script reads them; size |
| other phase-6 `.npz` (floors, grid secondary arms, Γ(t) and High re-evals) | 2245 | 103 MB | every number taken from them is in their eval JSON, which ships; size |
| renders and figures (`.gif`, `.png`) | 78 | 95 MB | paper-side; size |
| `paper/` | 547 | 39 MB | the paper ships separately. Its figure scripts read only shipped JSON/NPZ |
| `phase2_results/` | 35 | 4.7 MB | byte-identical duplicate of `che/bench/results/phase2/` (`diff -rq`) |
| `docs/decision_log.md` | 1 | 0.3 MB | quotes the owner; only through the switch |
| `CLAUDE.md`, `HANDOFF.md`, repo `README.md`, prompts, `phase6_design_v1.md`, red-team files, `docs/architecture_*`, venue reviews, other docs | 24 | 0.3 MB | not code, registration or a paper-number input. `CLAUDE.md` names the venue plan and "solo-researcher" |
| `post_v3_interaction/RUNBOOK.md` | 1 | 6 KB | owner-facing operations (deny list) |
| `m60/*.tar.zst` | 2 | 25 KB | raw spike archives |
| symlinks (`phase6/by_card/**`) | 13 | — | symlinks don't ship; `by_card/README.md` ships |
| checkpoints | — | — | gitignored and off-instance. Their hashes ship in `SHA256_CKPT.txt` |

## Scrub rules and rewrite log

The identity strings were found by grepping the repository:

- `git log --all --format='%an <%ae>'`: one human author handle and e-mail,
  plus the tool and GitHub noreply addresses;
- `LICENSE`;
- `git remote -v`: the GitHub URL and the repository name;
- `git branch -a`;
- the result files, which hold an absolute home path that includes the
  author's first name, host IPs, a GPU UUID and a cloud instance id.

The rules apply in order to every staged text file (`rules.SCRUBS`):

| id | match | replaced by |
|---|---|---|
| ABS-REPO | `/home\|/Users\|/root\|/workspace\|/mnt/…/<repo name>/` | removed (the path becomes repository-relative) |
| ABS-HOME / ABS-ROOT / ABS-WIN | other absolute home, `/root` or Windows user paths | `<abs-path>` |
| URL-GH / URL-CLAUDE | `github.com/…`, `claude.ai/…` | `<url-redacted>` |
| EMAIL / NAME-HANDLE / NAME | the author e-mail, handle, and name parts (whole words; Turkish ı handled) | `anonymous@example.org` / `Anonymous Authors` / `anonymous` |
| REPO | the repository name | `anonymous_repo` |
| BRANCH / SESSION | `claude/<words>` session branches, `paper-v2-phase1-wip`, `session_<id>` | `<branch>` / `session_<redacted>` |
| GPU-UUID | `GPU-xxxxxxxx-…` | `GPU-<uuid-redacted>` |
| IPV4 | dotted quads (port optional); **`uv.lock` exempt**, because its four-part package versions such as `12.9.2.10` look like IPs and redacting them breaks the lock | `<host>` |
| INSTANCE-ID | `id <7–10 digits>`, `instance id …` | `<instance-id>` |
| SSH-HOST | `root@<ip>` and similar | `<user@host>` |
| COMMIT | a 7–40-hex token that prefixes a commit in `git rev-list --all --reflog` | `COMMIT_REDACTED_NN` |
| COMMIT-CTX | a 40-hex token in a git context (`git`, `commit`, `shipped`, `HEAD`, `rev`, `sha`) even if this checkout lacks the commit. The phases 2–5 provenance commits are not in local history | `COMMIT_REDACTED_NN` |

The same commit always maps to the same placeholder, so cross-references stay
legible. `che/scripts/run_p6_s7_blocks.sh` and `che/tests/test_p6_s7_blocks.py`
both carry the frozen-base hash, and both get the same token. That keeps
`test_seed_counts_follow_the_ruling_and_the_locks` green; the git-diff test
skips without `.git`. Checkpoint, config and file sha256 values are 64-hex or
16-hex hashes of content, not commits, and stay.

The rewrite log of the run this README reports is in `scrub_log.tsv`, and its
counts are under "Check results" below.

## TMLR's size limit, verified

- **Source:** <https://jmlr.org/tmlr/author-guide.html>, read 2026-10-14
  (WebFetch, then the raw HTML with curl).
- **Quote:** "Authors may submit up to 100MB of supplementary material, such
  data, source code or illustrative videos; all supplementary materials must
  be in PDF or ZIP format." The same page also says: "Like submissions,
  supplementary material must be anonymized."
- **Reading:** `check_size.py` reads "100MB" conservatively, as 100 × 10⁶
  bytes.
- **Not verified:** the OpenReview form's own enforced limit. It is not
  visible without an account. OpenReview's generic docs use `maxSize: 50` as
  an example value, not as TMLR's setting. If the form refuses the zip, that
  is where to look.

## `docs/theory_foundations.md`: recommendation

**Recommendation: ship it** (default on). The reasons:

- App. A calls it "the formal specification".
- Every env module's docstring cites it by Def./Prop. number.
- The theory tests (invariant 4) are its propositions as code.

Without it, the supplement's citations dangle. The scrub found nothing
identifying in it. Two lines read as internal notes, not anonymity problems:
§10 "feeds the Claude Code prompts" and :771 "owner skims before". The owner
may want to see them; editing that file is not in this step's scope.

## What cannot be anonymized without changing meaning

1. **References to unshipped governance files.** About 60 comments and report
   lines cite `CLAUDE.md` or `docs/decision_log.md`, by rule name or date
   (e.g. "CLAUDE.md invariant #3"). They name the project's rulebook and
   betray an LLM-assisted workflow. The paper's disclosure states that
   anyway, and they identify no person. Removing them would change what the
   code says it obeys. They stay, and they dangle unless the owner ships
   decision-log excerpts.
2. **Dates and internal codes** (M5.5, G1.3, "RA", "the owner", "human-issued
   2026-07-28"). They do not identify anyone, and they are the audit trail.
3. **Hardware and provider.** "RTX 5090", "RTX PRO 6000", "vast.ai" (10
   mentions). These are methodological facts (floors are per-hardware).
4. **`post_v3_interaction/PLAN.md` mentions "a professor's review"**
   (PAPER V3 item 1(1)). That reveals review history, not identity. It is
   the orchestrator's file, and it is not rewritten here: PLAN.md is
   hash-pinned by the run (`plan_sha256`), so a rewrite would break that
   check for any reader. **Watch item:** if PLAN.md ever gains a commit hash
   or another scrub target, the scrub will change its bytes and its shipped
   hash will no longer match `plan_sha256`. Check `scrub_log.tsv` for
   `PLAN.md` after each build. In this build it had no rewrites.
5. **Commit placeholders.** The provenance in every result file now reads
   `COMMIT_REDACTED_NN`. A reviewer cannot check a result against a commit.
   This is the price of anonymity. The registration statement (V3-V2) should
   not imply that the supplement lets reviewers verify dates by commit.

## Findings for the record (reported, not fixed)

- **F1. The registered instruments cannot run on a fresh clone.**
  - `.gitignore:32` has `*.manifest`, a Python/PyInstaller template line.
    That pattern also matches the grid's `.manifest/` directories, so no
    `.manifest/<tag>.done` entry is committed. None exists in this working
    tree either.
  - `p6_unblind.load_arm`, `p6_post_analysis` and `p6_secondary.load_arm` all
    refuse without those entries.
  - The supplement rebuilds them from `SHA256_CKPT.txt`, which is the exact
    inverse of `lib_run_manifest.sh::manifest_write_aggregate`. The
    repository itself still cannot re-run its own instruments from a clone.
- **F2. The interaction-check analysis cannot run inside the supplement as
  written.**
  - `che/scripts/interaction_analysis.py` refuses unless PLAN.md is tracked by
    git and unchanged since its last commit. It also compares the run's
    `date_utc` with the plan's commit time.
  - The supplement has no `.git`, so a reader cannot recompute I.
  - **For the orchestrator:** consider a documented mode that checks
    PLAN.md's sha256 against the run's `plan_sha256:` without git, with the
    git-based checks recorded as skipped. Then add its command to
    `SHIPPED_README.md`.
- **F3. The registered instruments need `--allow-dirty` outside git**
  (`_git` returns "UNKNOWN"). That is documented in `SHIPPED_README.md`, and
  the outputs record it.

## Check results

Filled in from the run of `run_checks.sh` on 2026-10-14 (see below).
