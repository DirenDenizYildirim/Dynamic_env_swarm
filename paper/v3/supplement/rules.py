"""Selection and scrub rules for the anonymized code supplement (Paper v3, V3-V1).

Shared by `package.py` (which applies them to a STAGED COPY) and
`check_scrub.py` (which re-detects what must never ship). Nothing here touches
the source tree.

Selection is by RULE, not by a frozen file list, so the package can be rebuilt
at the end of the phase and pick up files added during it (new configs,
scripts, tests and `che/bench/results/phase6/post_v3_interaction/`).

The base set is what git would track: `git ls-files --cached --others
--exclude-standard` (tracked files plus untracked files that .gitignore does
not exclude). Symlinks are never shipped. A file enters the supplement iff it
matches an INCLUDE rule below; the first matching rule is recorded as its
reason. Everything else is left out, and the out/ selection log says why.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# ---------------------------------------------------------------- selection

P6 = "che/bench/results/phase6"

# Suffixes treated as text (scrubbed). Anything else is copied byte-for-byte
# and scanned for identity strings by check_scrub.py.
TEXT_SUFFIXES = {
    ".py",
    ".sh",
    ".yaml",
    ".yml",
    ".toml",
    ".lock",
    ".md",
    ".txt",
    ".json",
    ".jsonl",
    ".csv",
    ".sha256",
    ".cfg",
    ".ini",
    ".done",
    "",
}

# A single file larger than this is never shipped (reported instead).
MAX_FILE_BYTES = 20_000_000


@dataclass(frozen=True)
class Rule:
    rid: str
    pattern: str  # regex on the repo-relative POSIX path, full match
    why: str
    option: str | None = None  # name of the package.py switch that gates it


# Checked BEFORE the include rules: a match here never ships, whatever rule
# would otherwise take it.
DENY: tuple[tuple[str, str], ...] = (
    (
        r".*/post_v3_interaction[^/]*/(?:.*/)?RUNBOOK[^/]*",
        "owner-facing GPU runbook (laptop, backup, private-repo steps)",
    ),
)

INCLUDE: tuple[Rule, ...] = (
    # -- code: the che/ package, its configs, tests (incl. golden), scripts
    Rule(
        "C1",
        r"che/(?!bench/results/).*",
        "the che/ package: env, train, eval, calibration, bench code, configs, "
        "tests (incl. tests/golden), scripts",
    ),
    Rule(
        "C2",
        r"pyproject\.toml|uv\.lock",
        "install: the project metadata and the exact lock the suite ran under",
    ),
    Rule("C3", r"LICENSE", "licence text (copyright holder scrubbed)"),
    # -- documents
    Rule(
        "D1",
        r"docs/locks\.yaml",
        "the machine-readable lock registry; che/tests/test_locks.py, "
        "test_p6_grid.py and test_p6_s7_blocks.py read it",
    ),
    Rule(
        "D2",
        r"phase6_design_v2\.md|phase6_framing_branches\.md",
        "the registration documents (V3-V1)",
    ),
    Rule(
        "D3",
        r"docs/theory_foundations\.md",
        "the formal specification cited by every env docstring and by App. A",
        option="theory",
    ),
    Rule(
        "D4",
        r"(severity|coupling_a|kappa_b|comms)_lock\.md",
        "per-axis lock records; docs/locks.yaml cites them as the ruling "
        "documents of the locked constants",
        option="lock_records",
    ),
    # -- committed result artifacts
    Rule(
        "R5",
        re.escape(P6)
        + r"/post_v3_interaction[^/]*/(?!.*\.tar\.zst$)(?!(?:.*/)?RUNBOOK[^/]*$)"
        + r"(?!evals/eval_(?!(?:iso_s1|joint_s1|iso4_s1)_)[^/]*\.npz$).*",
        "the post hoc interaction check (plan, its timestamp proofs, evals, "
        "floors, report): what its --verify mode needs (PLAN §9). All files "
        "except .tar.zst archives (checkpoints; a results archive would "
        "duplicate the shipped files), the owner's RUNBOOK (operational "
        "instructions for renting the box; names the private repository), and "
        "the main evals' per-episode NPZ files other than the three floor "
        "checkpoints' (verification reads every main eval's JSON means, and "
        "per-episode arrays only for the floor; size)",
    ),
    Rule(
        "R1",
        r"che/bench/results/.*\.(md|txt|json|csv|sha256|yaml)",
        "every text result artifact of every phase: reports, eval summaries, "
        "provenance, timings, floors, hash lists (the ledger's sources)",
    ),
    Rule(
        "R2",
        r"che/bench/results/(phase[1-5]|e1|m05|m06)/.*\.npz",
        "calibration/ablation arrays of phases 1-5 (small; e.g. "
        "calibration_crossing.npz, estimates.npz)",
    ),
    Rule(
        "R3",
        re.escape(P6) + r"/(g1_conf_5090|g1_iso4_5090|g1_t2000_5090)/eval_[^/]*\.npz",
        "per-episode eval arrays of the policies the paper's results are "
        "about: ISO and JOINT (k=72), ISO-4 (k=20), T=2000 (k=4)",
    ),
    Rule(
        "R4",
        re.escape(P6) + r"/(g1_sec_s1_12_5090|g1_t2000_5090)/[^/]*\.jsonl"
        r"|" + re.escape(P6) + r"/g1_grid/(sweep|ident)_[^/]*_s(1[3-9]|20)\.jsonl",
        "training logs the registered instruments read (p6_secondary realized "
        "dose; p6_post_analysis T=2000 curves); established by tracing their "
        "file reads",
    ),
    Rule(
        "R6",
        re.escape(P6) + r"/g1_conf_5090/(iso|joint)_s[0-9]+\.jsonl",
        "training logs of the confirmatory arms (learning curves); no "
        "registered instrument reads them",
        option="conf_logs",
    ),
)

# Reasons recorded for notable exclusions (selection log only).
EXCLUDE_NOTES: tuple[tuple[str, str], ...] = (
    (r"phase2_results/.*", "byte-identical duplicate of che/bench/results/phase2/"),
    (
        r"che/bench/results/.*\.jsonl",
        "training/benchmark logs no paper-number script reads (size)",
    ),
    (r"che/bench/results/.*\.(gif|png)", "renders and figures (paper-side; size)"),
    (
        r"che/bench/results/.*\.npz",
        "per-episode arrays of floors, grid secondary arms, Gamma(t) and High "
        "re-evals; every paper number from them is in their eval JSON (size)",
    ),
    (r"che/bench/results/.*\.tar\.zst", "raw spike archives"),
    (r"docs/decision_log\.md", "quotes the owner; only via --decision-log-section"),
    (r"paper/.*", "the paper itself ships separately"),
    (
        r".*/post_v3_interaction[^/]*/(?:.*/)?RUNBOOK[^/]*",
        "owner-facing GPU runbook (laptop, backup, private-repo steps)",
    ),
    (r".*", "not code, registration, or a paper-number input"),
)

# ---------------------------------------------------------------- scrubbing
# Identity strings were found by grepping the repository: `git log --format=
# '%an %ae'`, LICENSE, `git remote -v`, the branch list, and the result files
# (absolute checkpoint paths, host IPs, a GPU UUID, a cloud instance id).

REPO_NAME = r"Dynamic[_ -]env[_ -]swarm"

NAME_PATTERNS = (
    r"direndenizyildirim2008@gmail\.com",
    r"direndenizyildirim",
    r"\bdiren\b",
    r"\bdeniz\b",
    r"y[iı]ld[iı]r[iı]m",
)

WIN_ABS = (
    r"(?<![\w])[A-Za-z]:\\{1,2}"
    r"(?:Users|Documents and Settings|home|Program Files|Windows)\b"
)

HEX_TOKEN = re.compile(r"(?<![0-9A-Za-z])([0-9a-f]{7,40})(?![0-9A-Za-z])")
GIT_CONTEXT_40 = re.compile(
    r"(?i)(?:git|commit|shipped|head|rev|sha)\W{0,4}[^\n]{0,24}?"
    r"(?<![0-9a-f])([0-9a-f]{40})(?![0-9a-f])"
)


@dataclass(frozen=True)
class Scrub:
    rid: str
    regex: re.Pattern
    repl: str  # replacement for the whole match
    why: str
    skip: str | None = None  # regex on the path of files this rule ignores


def _c(p: str, flags: int = re.IGNORECASE) -> re.Pattern:
    return re.compile(p, flags)


# Applied in order. Commit hashes are handled separately (they need the
# repository's commit list), after these.
SCRUBS: tuple[Scrub, ...] = (
    Scrub(
        "ABS-REPO",
        _c(
            r"(?:/home|/Users|/root|/workspace|/mnt)/[^\s\"'`:,;]*?" + REPO_NAME + r"/?"
        ),
        "",
        "absolute path into the checkout -> repository-relative",
    ),
    Scrub(
        "ABS-HOME",
        _c(r"(?<![\w.~$-])(?:/home|/Users)/[^\s\"'`),;]*"),
        "<abs-path>",
        "absolute home path",
    ),
    Scrub(
        "ABS-ROOT",
        _c(r"(?<![\w.~$-])/root/[^\s\"'`),;]*"),
        "<abs-path>",
        "absolute /root path",
    ),
    Scrub("ABS-WIN", _c(WIN_ABS + r"[^\s\"']*"), "<abs-path>", "absolute Windows path"),
    Scrub(
        "URL-GH",
        _c(r"(?:https?://)?(?:www\.)?github\.com/[^\s)\]>\"'`]*"),
        "<url-redacted>",
        "GitHub URL",
    ),
    Scrub(
        "URL-CLAUDE",
        _c(r"(?:https?://)?claude\.ai/[^\s)\]>\"'`]*"),
        "<url-redacted>",
        "session/artifact URL",
    ),
    Scrub("EMAIL", _c(NAME_PATTERNS[0]), "anonymous@example.org", "author email"),
    Scrub("NAME-HANDLE", _c(NAME_PATTERNS[1]), "Anonymous Authors", "author handle"),
    Scrub("NAME", _c("|".join(NAME_PATTERNS[2:])), "anonymous", "author name parts"),
    Scrub("REPO", _c(REPO_NAME), "anonymous_repo", "repository name"),
    Scrub(
        "BRANCH",
        _c(r"\bclaude/[a-z0-9]+(?:-[a-z0-9]+)+\b|\bpaper-v2-phase1-wip\b"),
        "<branch>",
        "session branch name",
    ),
    Scrub(
        "SESSION",
        _c(r"\bsession_[A-Za-z0-9]{16,}\b", 0),
        "session_<redacted>",
        "session id",
    ),
    Scrub(
        "GPU-UUID",
        _c(r"\bGPU-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
        "GPU-<uuid-redacted>",
        "GPU serial UUID",
    ),
    Scrub(
        "IPV4",
        re.compile(
            r"(?<![\d.])(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}"
            r"(?:25[0-5]|2[0-4]\d|1?\d?\d)(?::\d{2,5})?(?![\d.])"
        ),
        "<host>",
        "host IP[:port]",
        skip=r"uv\.lock",
    ),  # uv.lock: four-part package versions, not hosts
    Scrub(
        "INSTANCE-ID",
        _c(r"(?<=\bid )\d{7,10}\b|(?<=instance[ _-]id[:= ])\s*\d{6,10}\b"),
        "<instance-id>",
        "cloud instance id",
    ),
    Scrub(
        "SSH-HOST",
        _c(
            r"\b(?:root|ubuntu|user)@(?:\d{1,3}\.){3}\d{1,3}\b|\b(?:root|ubuntu)@ssh\d*\.[\w.-]+"
        ),
        "<user@host>",
        "ssh login",
    ),
)

# check_scrub.py: patterns that must NOT appear anywhere in the shipped tree
# (text and binary). A hit is a FAIL. Entries: (name, regex[, skip-path regex]).
FORBIDDEN: tuple[tuple, ...] = (
    ("name/handle/email", _c("|".join(NAME_PATTERNS))),
    ("repository name", _c(REPO_NAME)),
    ("GitHub URL", _c(r"github\.com/")),
    ("claude.ai URL", _c(r"claude\.ai/")),
    ("absolute path", _c(r"(?<![\w.~$-])(?:/home/|/root/|/Users/)|" + WIN_ABS)),
    ("session branch", _c(r"\bclaude/[a-z0-9]+(?:-[a-z0-9]+)+\b|paper-v2-phase1-wip")),
    ("session id", re.compile(r"\bsession_[A-Za-z0-9]{16,}\b")),
    ("GPU UUID", _c(r"GPU-[0-9a-f]{8}-[0-9a-f]{4}-")),
    (
        "IPv4",
        re.compile(
            r"(?<![\d.])(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}"
            r"(?:25[0-5]|2[0-4]\d|1?\d?\d)(?![\d.])"
        ),
        r"uv\.lock",
    ),
    (
        "email",
        re.compile(r"[A-Za-z0-9._%+-]+@(?!example\.org)[A-Za-z0-9-]+\.[A-Za-z.]{2,}"),
    ),
)

# Reported for a human look, not failed.
WARN: tuple[tuple[str, re.Pattern], ...] = (
    ("host field", _c(r"\bhost(?:name)?\s*[:=]\s*(?!<host>)\S+")),
    ("instance id context", _c(r"(?:instance|vast)[^\n]{0,40}\b\d{7,10}\b")),
    ("40-hex in a git context", GIT_CONTEXT_40),
)

# Allowed e-mail-like strings (none needed so far).
EMAIL_ALLOW: tuple[str, ...] = ("anonymous@example.org",)
