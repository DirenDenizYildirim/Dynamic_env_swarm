"""The v3 main-text checks (builder B2, Paper v3 step 3; ``paper_v3_prompt.md`` V3-S1, S2,
S3, S5 and planner P2's print-legibility recommendation).

Five checks, each runnable on its own and each wired into ``build_v3.py`` (source side) or
``kit_report.py`` (printed-PDF side):

- ``pages``       main-text printed pages <= a ceiling (default 15), measured on the kit's
                  printed PDF: ``pdftotext -bbox-layout`` heading positions, position =
                  (page - 1) + y / page height. Two readings are always reported: from the
                  top of page 1, and from the first numbered H2 ("1 ..."); both end at the
                  first appendix H2. Which reading is graded is ``--grade``.
- ``terms``       no internal code or private-vocabulary term in the main text, from a
                  term list (``paper/v3/checks/terms.txt``, builder B1's; the seed in
                  ``checks_seed/`` until it exists). Appendix exempt; registered strings
                  exempt where they appear verbatim.
- ``dates``       no date in the main text outside an allow-list
                  (``paper/v3/checks/dates_allow.txt``, B1's; seeded likewise).
- ``caveats``     each caveat of the one-home map (``paper/v3/checks/caveats.yaml``, B1's)
                  is stated in its home file and nowhere else in the body; a pointer to
                  the home is allowed.
- ``legibility``  every printed figure image: estimated printed label size =
                  nominal label size x printed width / source width, against a minimum.

"Main text" is everything from the top of the paper to the first H2 that matches
``--appendix-re`` (default ``^Appendi``): the front matter's title and description, the
abstract, and every section before that heading. What a reader sees is scanned: HTML
comments, tag markup, link targets, Liquid paths and ``<d-cite>`` keys are masked;
captions, ``alt`` and ``title`` text, inline code, math and listings are kept (a listing
hit is labelled ``code``).

Usage (repository root; ``$PY`` has pyyaml):

    $PY paper/v3/src/v3_checks.py terms   [--root DIR] [--terms FILE] [--json OUT]
    $PY paper/v3/src/v3_checks.py dates   [--root DIR] [--allow FILE] [--json OUT]
    $PY paper/v3/src/v3_checks.py caveats [--root DIR] [--caveats FILE] [--json OUT]
    $PY paper/v3/src/v3_checks.py pages   --pdf FILE [--root DIR] [--max-pages 15]
                                          [--grade page1|section1] [--json OUT]
    $PY paper/v3/src/v3_checks.py legibility --pdf FILE --kit-source MD --files JSON
                                          [--label-pt 8] [--min-pt 7] [--json OUT]

Each exits 1 on FAIL, 0 on PASS, and 0 with "NOT CONFIGURED" when its input list does not
exist. See ``README.md`` ("v3 checks") for the file formats and what each is blind to.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

sys.dont_write_bytecode = True  # keep src/ free of __pycache__

SRC = Path(__file__).resolve().parent
ROOT = SRC.parents[2]
V3 = ROOT / "paper" / "v3"
CHECKS = V3 / "checks"
SEED = SRC / "checks_seed"
APPENDIX_RE = r"^Appendi"
START_RE = r"^1\s"

# B1's lists, and the seeds used while they do not exist.
DEFAULTS = {
    "terms": (CHECKS / "terms.txt", SEED / "terms.seed.txt"),
    "dates": (CHECKS / "dates_allow.txt", SEED / "dates_allow.seed.txt"),
    "registered": (CHECKS / "registered.txt", SEED / "registered.seed.txt"),
    "caveats": (CHECKS / "caveats.yaml", None),
}


def default_list(kind: str) -> Path | None:
    own, seed = DEFAULTS[kind]
    if own.exists():
        return own
    return seed if seed is not None and seed.exists() else None


def rel(p: Path) -> str:
    try:
        return str(Path(p).resolve().relative_to(ROOT))
    except ValueError:
        return str(p)


# ------------------------------------------------------------- visible text


@dataclass
class Part:
    """One source file (or the front matter) as a reader sees it."""

    name: str
    raw: str
    vis: str = ""  # same length as raw; masked chars are spaces
    code: list = field(default_factory=list)  # (start, end) offsets of fenced code
    limit: int | None = None  # main text ends at this offset (None: whole file)
    appendix: bool = False  # the whole file is appendix
    nocomment: str = ""  # raw with HTML comments blanked (same length)

    def line_of(self, off: int) -> int:
        return self.raw.count("\n", 0, off) + 1

    def in_code(self, off: int) -> bool:
        return any(a <= off < b for a, b in self.code)


VISIBLE_ATTRS = {"alt", "title", "caption", "aria-label"}
FENCE_RE = re.compile(r"(?ms)^ {0,3}(`{3,}|~{3,})[^\n]*\n.*?^ {0,3}\1[ \t]*$")
TAG_RE = re.compile(r"</?[A-Za-z][A-Za-z0-9-]*(?:\s[^<>]*)?/?>", re.S)
LIQ_INC_RE = re.compile(r"\{%.*?%\}", re.S)
LIQ_REL_RE = re.compile(r"\{\{.*?\}\}", re.S)
ATTR_RE = re.compile(r'([\w-]+)\s*=\s*"([^"]*)"|([\w-]+)\s*=\s*\'([^\']*)\'')


def _blank(s: str) -> str:
    return re.sub(r"[^\n]", " ", s)


def _keep_attrs(tok: str) -> str:
    """Blank a tag or Liquid include, keeping the values of reader-visible attributes."""
    out = list(_blank(tok))
    for m in ATTR_RE.finditer(tok):
        name = (m.group(1) or m.group(3) or "").lower()
        if name in VISIBLE_ATTRS:
            g = 2 if m.group(1) else 4
            a, b = m.span(g)
            out[a:b] = tok[a:b]
    return "".join(out)


def visible(raw: str) -> tuple[str, list[tuple[int, int]]]:
    """Mask what a reader never sees, keeping every offset (and so every line number)."""
    s = re.sub(r"<!--.*?-->", lambda m: _blank(m.group(0)), raw, flags=re.S)
    code = []
    for m in FENCE_RE.finditer(s):
        a, b = m.span()
        first_nl = s.index("\n", a)
        last_nl = s.rfind("\n", a, b)
        code.append((first_nl + 1, last_nl if last_nl > first_nl else b))
        s = (
            s[:a]
            + _blank(s[a:first_nl])
            + s[first_nl : last_nl + 1]
            + _blank(s[last_nl + 1 : b])
            + s[b:]
        )

    def outside_code(fn):
        def sub(m):
            if any(a <= m.start() < b for a, b in code):
                return m.group(0)
            return fn(m.group(0))

        return sub

    s = LIQ_INC_RE.sub(outside_code(_keep_attrs), s)
    s = LIQ_REL_RE.sub(outside_code(_blank), s)
    s = TAG_RE.sub(outside_code(_keep_attrs), s)
    # markdown link and image targets: [text](target) -> keep text
    s = re.sub(r"(\]\()([^)\s]*)(\))", lambda m: " " * len(m.group(0)), s)
    return s, code


def normalize(vis: str) -> tuple[str, list[int]]:
    """Collapse whitespace runs to one space; return the text and a map to raw offsets."""
    out, idx, prev_space = [], [], False
    for i, ch in enumerate(vis):
        if ch.isspace():
            if prev_space:
                continue
            out.append(" ")
            idx.append(i)
            prev_space = True
        else:
            out.append(ch)
            idx.append(i)
            prev_space = False
    idx.append(len(vis))
    return "".join(out), idx


def section_files(root: Path) -> list[Path]:
    return sorted((root / "sections").glob("*.md"))


@dataclass
class Scope:
    """What counts as main text. A file is appendix if it is listed in ``appendix_files``
    (the one-home map's list, when it has one) or if it holds, or follows, an H2 matching
    ``appendix_re``; in the file that holds that H2, main text ends at the heading."""

    appendix_re: str = APPENDIX_RE
    main_files: list | None = None
    appendix_files: list | None = None
    source: str = "headings"


def scope_from_map(path: Path | None, appendix_re: str = APPENDIX_RE) -> Scope:
    sc = Scope(appendix_re)
    if path is None or not Path(path).exists():
        return sc
    try:
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return sc
    if isinstance(data, dict) and (
        data.get("main_text_files") or data.get("appendix_files")
    ):
        sc.main_files = [file_key(x) for x in data.get("main_text_files") or []]
        sc.appendix_files = [file_key(x) for x in data.get("appendix_files") or []]
        sc.source = (
            f"{rel(path)} (main_text_files, appendix_files) and H2 {appendix_re!r}"
        )
    return sc


def load_parts(
    root: Path,
    sections: list[tuple[str, str]] | None = None,
    scope: Scope | str | None = None,
    front_matter: dict | None = None,
    appendix_re: str | None = None,
) -> list[Part]:
    """The paper's parts in build order, each marked main text or appendix.

    ``sections`` is a list of (name, raw text); by default ``<root>/sections/*.md``.
    The front matter's ``title`` and ``description`` (from ``front_matter`` or
    ``<root>/front_matter.yaml``) come first, as the part ``front_matter.yaml``.
    """
    if scope is None or isinstance(scope, str):
        scope = Scope(scope or appendix_re or APPENDIX_RE)
    if sections is None:
        sections = [
            (p.name, p.read_text(encoding="utf-8")) for p in section_files(root)
        ]
    if front_matter is None:
        fmp = root / "front_matter.yaml"
        try:
            front_matter = (
                yaml.safe_load(fmp.read_text(encoding="utf-8")) if fmp.exists() else {}
            )
        except yaml.YAMLError:
            front_matter = {}
    parts = []
    fm_text = "\n".join(
        str((front_matter or {}).get(k, "")) for k in ("title", "description")
    )
    if fm_text.strip():
        parts.append(Part("front_matter.yaml", fm_text))
    in_appendix = False
    listed_app = set(scope.appendix_files or [])
    listed_main = set(scope.main_files or [])
    for name, raw in sections:
        p = Part(name, raw)
        if name in listed_app or (in_appendix and name not in listed_main):
            p.appendix = True
        else:
            vis, code = visible(raw)
            for m in re.finditer(r"(?m)^##[ \t]+(.*?)[ \t]*#*[ \t]*$", vis):
                if not any(x <= m.start() < y for x, y in code) and re.search(
                    scope.appendix_re, m.group(1).strip()
                ):
                    p.limit = m.start()
                    in_appendix = True
                    break
        parts.append(p)
    for p in parts:
        p.vis, p.code = visible(p.raw)
        p.nocomment = re.sub(
            r"<!--.*?-->", lambda m: _blank(m.group(0)), p.raw, flags=re.S
        )
    return parts


def unlisted_files(parts: list[Part], scope: Scope) -> list[str]:
    if scope.main_files is None and scope.appendix_files is None:
        return []
    known = set(scope.main_files or []) | set(scope.appendix_files or [])
    return [
        p.name for p in parts if p.name != "front_matter.yaml" and p.name not in known
    ]


def main_text_offsets(p: Part) -> int:
    """Offset where main text ends in this part (0 if the part is appendix)."""
    if p.appendix:
        return 0
    return len(p.raw) if p.limit is None else p.limit


def context(norm: str, a: int, b: int, width: int = 50) -> str:
    return (
        ("…" if a > width else "")
        + norm[max(0, a - width) : b + width].strip()
        + ("…" if b + width < len(norm) else "")
    )


def strip_note(line: str) -> tuple[str, str]:
    """Split 'pattern<TAB>options' or 'pattern  # note' into (pattern, rest)."""
    if "\t" in line:
        a, b = line.split("\t", 1)
        return a.strip(), b.strip()
    m = re.search(r"\s{2,}#\s?|\s+—\s+", line)
    if m:
        return line[: m.start()].strip(), line[m.end() :].strip()
    return line.strip(), ""


def phrase_regex(text: str, case: bool = False) -> re.Pattern:
    body = r"\s+".join(re.escape(w) for w in text.split())
    lead = r"\b" if re.match(r"\w", text) else ""
    tail = r"\b" if re.search(r"\w$", text) else ""
    return re.compile(lead + body + tail, 0 if case else re.I)


# ------------------------------------------------------------------ terms


@dataclass
class Term:
    label: str
    rx: re.Pattern
    note: str = ""


def read_list_lines(path: Path) -> list[str]:
    """Non-blank lines that do not start with '#' (leading spaces kept out)."""
    return [
        raw.rstrip("\n")
        for raw in path.read_text(encoding="utf-8").splitlines()
        if raw.strip() and not raw.lstrip().startswith("#")
    ]


def parse_terms(path: Path) -> tuple[list[Term], list[str]]:
    """Term list format, as builder B1 fixed it in ``paper/v3/checks/terms.txt``:

    - one Python ``re`` pattern per non-comment line; lines starting with ``#`` and blank
      lines are ignored;
    - an optional note after a single TAB (printed with a hit; patterns hold no TAB);
    - case-sensitive unless the pattern starts with ``(?i)``.

    Returns (terms, parse problems).
    """
    terms, problems = [], []
    for line in read_list_lines(path):
        pat, _, note = line.partition("\t")
        pat = pat.strip()
        try:
            rx = re.compile(pat)
        except re.error as e:
            problems.append(f"{pat!r}: {e}")
            continue
        if rx.search(""):
            problems.append(f"{pat!r} matches the empty string")
            continue
        terms.append(Term(pat, rx, note.strip()))
    return terms, problems


def read_registered(path: Path | None) -> list[str]:
    """Registered strings, one per line, '#' comments; a TAB starts a note."""
    if path is None or not path.exists():
        return []
    return [ln.partition("\t")[0].strip() for ln in read_list_lines(path)]


def exempt_spans(norm: str, strings: list[str]) -> list[tuple[int, int, str]]:
    spans = []
    for s in strings:
        rx = r"\s+".join(re.escape(w) for w in s.split())
        for m in re.finditer(rx, norm):
            spans.append((m.start(), m.end(), s))
    return spans


CAPTION_RES = [
    re.compile(r"<figcaption\b[^>]*>(.*?)</figcaption>", re.S | re.I),
    re.compile(
        r"<p\b[^>]*class=\"[^\"]*\bcaption\b[^\"]*\"[^>]*>(.*?)</p>", re.S | re.I
    ),
    re.compile(r"\bcaption=\"([^\"]*)\""),
    re.compile(r"(?m)^\*\*(?:Figure|Table)\s+[A-Z]?\d+\.\*\*(.*)$"),
]
GLOSS_RE = re.compile(r"labelled\s+\u201c([^\u201d]+)\u201d\s+on\s+the\s+figure")


def caption_spans(raw: str) -> list[tuple[int, int]]:
    """Raw offsets of figure-caption text: <figcaption>, <p class="caption">, an include's
    caption attribute, or a '**Figure N.**' caption paragraph."""
    return [m.span(1) for rx in CAPTION_RES for m in rx.finditer(raw)]


def run_terms(parts: list[Part], terms: list[Term], registered: list[str]) -> dict:
    """Every term match in the main text is a hit, except:

    - inside a registered string that must appear verbatim (``registered``): exempt;
    - inside a figure-label gloss (B1's rule, terms.txt EXEMPTION): the exact form
      ``labelled \u201cTERM\u201d on the figure`` inside a figure caption. Each glossed
      term may be glossed once in the whole main text; the first gloss is valid, a later
      gloss of the same term is not, and its matches are hits;
    - inside fenced code (a listing): listed, not graded (terms.txt SCOPE strips code).
    """
    prepared, gloss_count = [], {}
    for p in parts:  # first pass: the glosses, in document order
        end = main_text_offsets(p)
        if end == 0:
            continue
        norm, idx = normalize(p.vis[:end])
        caps = caption_spans(p.raw[:end])
        gl = []
        for m in GLOSS_RE.finditer(norm):
            if any(a <= idx[m.start()] < b for a, b in caps):
                gloss_count[m.group(1)] = gloss_count.get(m.group(1), 0) + 1
                gl.append(
                    (m.start(), m.end(), m.group(1), gloss_count[m.group(1)] == 1)
                )
        prepared.append((p, norm, idx, gl, exempt_spans(norm, registered)))
    hits, exempt, glossed, in_code = [], [], [], []
    for p, norm, idx, gl, ex in prepared:
        for t in terms:
            for m in t.rx.finditer(norm):
                if m.end() == m.start():
                    continue
                off = idx[m.start()]
                rec = {
                    "term": t.label,
                    "note": t.note,
                    "where": f"{p.name}:{p.line_of(off)}",
                    "match": m.group(0),
                    "context": context(norm, m.start(), m.end()),
                }
                if p.in_code(off):
                    in_code.append(rec)
                    continue
                cover = next(
                    (s for a, b, s in ex if a <= m.start() and m.end() <= b), None
                )
                if cover:
                    rec["exempt_by"] = cover
                    exempt.append(rec)
                    continue
                g = next((x for x in gl if x[0] <= m.start() and m.end() <= x[1]), None)
                if g and g[3]:
                    rec["gloss"] = g[2]
                    glossed.append(rec)
                    continue
                if g:
                    rec["why"] = f"a second gloss of \u201c{g[2]}\u201d"
                hits.append(rec)
    per_term: dict[str, int] = {}
    for h in hits:
        per_term[h["term"]] = per_term.get(h["term"], 0) + 1
    return {
        "terms": len(terms),
        "registered": len(registered),
        "hits": hits,
        "exempt_registered": exempt,
        "glossed": glossed,
        "in_code_not_graded": in_code,
        "gloss_count": gloss_count,
        "per_term": per_term,
        "status": "PASS" if not hits else "FAIL",
    }


# ------------------------------------------------------------------ dates

MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}
MON = (
    r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|"
    r"Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
)
YEAR = r"(?:19|20)\d\d"
CONTEXT_WORDS = (
    r"(?:in|on|since|by|until|till|before|after|from|during|through|to|"
    r"early|mid|late|end\s+of|start\s+of|spring|summer|autumn|fall|winter|"
    r"dated|registered|ruled|unblinded|run|ran)"
)
DATE_PATTERNS = [
    (
        "iso",
        re.compile(
            rf"\b(?P<y>{YEAR})-(?P<m>0[1-9]|1[0-2])-(?P<d>0[1-9]|[12]\d|3[01])\b"
        ),
    ),
    (
        "iso-range-end",
        re.compile(
            r"(?<=\d)\s?(?:→|–|-|to)\s?(?P<m>0[1-9]|1[0-2])-(?P<d>0[1-9]|[12]\d|3[01])\b"
            r"(?!-)"
        ),
    ),
    (
        "month-day-year",
        re.compile(
            rf"\b(?P<mon>{MON})\.?\s+(?P<d>[0-3]?\d)(?:st|nd|rd|th)?,?\s+(?P<y>{YEAR})\b"
        ),
    ),
    (
        "day-month-year",
        re.compile(
            rf"\b(?P<d>[0-3]?\d)(?:st|nd|rd|th)?\s+(?P<mon>{MON})\.?,?\s+(?P<y>{YEAR})\b"
        ),
    ),
    ("iso-month", re.compile(rf"\b(?P<y>{YEAR})-(?P<m>0[1-9]|1[0-2])\b(?![-\d])")),
    ("month-year", re.compile(rf"\b(?P<mon>{MON})\.?,?\s+(?P<y>{YEAR})\b")),
    (
        "month-day",
        re.compile(
            rf"\b(?P<mon>{MON})\.?\s+(?P<d>[0-3]?\d)(?:st|nd|rd|th)?\b(?![\d.,]\d)"
        ),
    ),
    ("day-month", re.compile(rf"\b(?P<d>[0-3]?\d)(?:st|nd|rd|th)?\s+(?P<mon>{MON})\b")),
]
# Bare years count as dates only for the project's own years, after a date word ("in 2026",
# "by early 2026"): citations print years ("Gao et al. (2024)") and must pass (B1's
# dates_allow.txt). Every other bare year is listed, not graded.
CONTEXT_YEARS = ["2025", "2026"]


def year_in_context_re(years: list[str]) -> re.Pattern:
    alt = "|".join(re.escape(y) for y in years)
    return re.compile(
        rf"\b{CONTEXT_WORDS}\s+(?:of\s+|the\s+|early\s+|mid-?\s*|late\s+)?"
        rf"(?P<y>{alt})\b(?![-–.]?\d)",
        re.I,
    )


BARE_YEAR = re.compile(
    r"(?<![\w.$-])(20[0-4]\d)(?![\w.%-]|\s?(?:pages?|episodes?|updates?|steps?|seeds?))"
)


def date_key(kind: str, g: dict) -> str:
    """Normalize a matched date: YYYY-MM-DD, YYYY-MM, YYYY, --MM-DD (no year)."""
    m = g.get("m")
    if g.get("mon"):
        m = f"{MONTHS[g['mon'][:3].lower()]:02d}"
    d = f"{int(g['d']):02d}" if g.get("d") else None
    y = g.get("y")
    if y and m and d:
        return f"{y}-{m}-{d}"
    if y and m:
        return f"{y}-{m}"
    if m and d:
        return f"--{m}-{d}"
    return y or "?"


def parse_allow(path: Path | None) -> tuple[list[str], list[re.Pattern]]:
    keys, rxs = [], []
    if path is None or not path.exists():
        return keys, rxs
    for line in read_list_lines(path):
        pat, _ = strip_note(line)
        if pat.startswith("re:"):
            rxs.append(re.compile(pat[3:]))
            continue
        hit = None
        for kind, rx in DATE_PATTERNS:
            m = rx.fullmatch(pat)
            if m:
                hit = date_key(kind, m.groupdict())
                break
        keys.append(hit or pat)
    return keys, rxs


def allowed(key: str, text: str, keys: list[str], rxs: list[re.Pattern]) -> bool:
    if text in keys or key in keys or any(r.search(text) for r in rxs):
        return True
    if key.startswith("--"):  # month and day only: allowed if an allowed date has them
        return any(
            k.endswith(key[1:]) for k in keys if re.fullmatch(r"\d{4}-\d\d-\d\d", k)
        )
    return False


def run_dates(
    parts: list[Part],
    keys: list[str],
    rxs: list[re.Pattern],
    context_years: list[str] | None = None,
) -> dict:
    hits, ok, bare, in_code = [], [], [], []
    patterns = DATE_PATTERNS + [
        ("year-in-context", year_in_context_re(context_years or CONTEXT_YEARS))
    ]
    for p in parts:
        end = main_text_offsets(p)
        if end == 0:
            continue
        norm, idx = normalize(p.vis[:end])
        taken: list[tuple[int, int]] = []
        for kind, rx in patterns:
            for m in rx.finditer(norm):
                if any(a < m.end() and m.start() < b for a, b in taken):
                    continue
                g = m.groupdict()
                if (
                    kind == "iso-range-end"
                ):  # '2026-09-09 → 09-22': the year of the start
                    prev = re.search(rf"({YEAR})-\d\d-\d\d\s?$", norm[: m.start()])
                    if not prev:
                        continue
                    g = {**g, "y": prev.group(1)}
                taken.append(m.span())
                key = date_key(kind, g)
                off = idx[m.start()]
                rec = {
                    "date": key,
                    "kind": kind,
                    "match": m.group(0).strip(),
                    "where": f"{p.name}:{p.line_of(off)}",
                    "in": "code" if p.in_code(off) else "text",
                    "context": context(norm, m.start(), m.end()),
                }
                if allowed(key, m.group(0).strip(), keys, rxs):
                    ok.append(rec)
                elif rec["in"] == "code":  # listings: listed, not graded (B1's SCOPE)
                    in_code.append(rec)
                else:
                    hits.append(rec)
        for m in BARE_YEAR.finditer(norm):
            if any(a <= m.start() < b for a, b in taken):
                continue
            off = idx[m.start()]
            bare.append(
                {
                    "year": m.group(1),
                    "where": f"{p.name}:{p.line_of(off)}",
                    "context": context(norm, m.start(), m.end(), 35),
                }
            )
    return {
        "allow": keys + [r.pattern for r in rxs],
        "context_years": context_years or CONTEXT_YEARS,
        "hits": hits,
        "allowed": ok,
        "in_code_not_graded": in_code,
        "bare_years_not_graded": bare,
        "status": "PASS" if not hits else "FAIL",
    }


# ---------------------------------------------------------------- caveats


def heading_ids(raw: str) -> set[str]:
    sys.path.insert(0, str(SRC))
    import distill_port as dp  # noqa: E402

    vis, code = visible(raw)
    out = set()
    for m in re.finditer(r"(?m)^#{1,6}[ \t]+(.*?)[ \t]*#*[ \t]*$", vis):
        if not any(a <= m.start() < b for a, b in code):
            out.add(dp.kramdown_id(m.group(1)))
    out |= set(re.findall(r'\bid="([^"]+)"', raw))
    return out


def as_list(v) -> list:
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def file_key(s: str) -> str:
    s = Path(str(s)).name
    return s if s.endswith(".md") or s == "front_matter.yaml" else s + ".md"


def _compile(pats, cid, problems) -> list[re.Pattern]:
    out = []
    for pat in as_list(pats):
        try:
            out.append(re.compile(str(pat)))
        except re.error as e:
            problems.append(f"{cid}: bad regex {pat!r}: {e}")
    return out


def parse_caveats(path: Path) -> tuple[list[dict], list[str]]:
    """The one-home map, in builder B1's format (``paper/v3/checks/caveats.yaml``):

    a top key ``caveats`` holding a list of entries (a mapping id -> entry also works), each
    with ``id``; ``home`` (a file, or a list of files); ``regex`` (a list of Python
    patterns, case-sensitive unless a pattern starts with ``(?i)``); optional ``also``
    (files allowed ``max_also`` occurrences each, default 1); optional ``max_home``
    (default 1). An entry with ``kind: label_required`` has ``trigger`` and ``label``
    pattern lists instead. Optional top keys ``main_text_files`` and ``appendix_files``
    define the main text (see ``Scope``). Aliases: ``patterns``/``regexes``/``match`` for
    ``regex``; ``home_file``; ``allowed_in``/``exceptions``/``allow_also`` for ``also``.
    """
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if isinstance(data, dict) and isinstance(data.get("caveats"), (dict, list)):
        data = data["caveats"]
    items = (
        data.items()
        if isinstance(data, dict)
        else [(d.get("id"), d) for d in data if isinstance(d, dict)]
    )
    out, problems = [], []
    for cid, spec in items:
        if not isinstance(spec, dict):
            problems.append(f"{cid}: not a mapping")
            continue
        kind = spec.get("kind", "one_home")
        rec = {"id": str(cid), "name": spec.get("name", ""), "kind": kind}
        if kind == "label_required":
            rec["trigger"] = _compile(spec.get("trigger"), cid, problems)
            rec["label"] = _compile(spec.get("label"), cid, problems)
            if not rec["trigger"] or not rec["label"]:
                problems.append(
                    f"{cid}: label_required needs trigger and label patterns"
                )
            out.append(rec)
            continue
        home = as_list(spec.get("home", spec.get("home_file")))
        pats = spec.get(
            "regex", spec.get("patterns", spec.get("regexes", spec.get("match")))
        )
        also = as_list(
            spec.get(
                "also",
                spec.get("allowed_in", spec.get("exceptions", spec.get("allow_also"))),
            )
        )
        rec.update(
            home=[file_key(h) for h in home if h],
            also=[file_key(x) for x in also],
            rxs=_compile(pats, cid, problems),
            patterns=[str(x) for x in as_list(pats)],
            max_home=int(spec.get("max_home", 1)),
            max_also=int(spec.get("max_also", 1)),
        )
        if not rec["home"]:
            problems.append(f"{cid}: no home")
        if not rec["rxs"]:
            problems.append(f"{cid}: no patterns")
        out.append(rec)
    return out, problems


# Sentence boundaries, as provenance_check.split_sentences draws them (abbreviations,
# initials and math are not ends).
SENT_SPLIT = re.compile(
    r"(?<=[.!?])[\"”’)]?\s+(?=[\"“(§\[]?[A-Z0-9ΓΔΘΛΞΠΣΦΨΩαβγδεκλμνξπρστφχψω])"
)


def _abbrevs() -> tuple[list[str], list[str]]:
    sys.path.insert(0, str(SRC))
    try:
        from provenance_check import ABBREV, ABBREV_BEFORE_NUMBER  # noqa: E402

        return ABBREV, ABBREV_BEFORE_NUMBER
    except Exception:  # noqa: BLE001  (the build venv lacks nothing; a bare venv may)
        return (
            [
                "e.g.",
                "i.e.",
                "et al.",
                "Fig.",
                "Eq.",
                "App.",
                "Def.",
                "Prop.",
                "Thm.",
                "Cor.",
                "Sec.",
                "vs.",
                "cf.",
                "approx.",
                "Tab.",
                "resp.",
            ],
            ["pp.", "p.", "No."],
        )


@dataclass
class Unit:
    """One sentence, table cell or caption: raw offsets, and its paragraph's."""

    a: int
    b: int
    pa: int
    pb: int
    kind: str


def _sentences(p: Part, a: int, b: int, pa: int, pb: int, out: list, abbrev) -> None:
    norm, idx = normalize(p.vis[a:b])
    if not re.search(r"\w", norm):
        return
    ab, abn = abbrev
    cuts = [0]
    for m in SENT_SPLIT.finditer(norm):
        before = norm[: m.start() + 1]
        if before.count("$") % 2:  # inside math
            continue
        if any(
            before.endswith(x)
            and (len(before) == len(x) or not before[-len(x) - 1].isalnum())
            for x in ab
        ):
            continue
        if any(
            before.endswith(x) and re.match(r"\s?\d", norm[m.end() : m.end() + 2] or "")
            for x in abn
        ):
            continue
        if re.search(r"(?:^|\s)[A-Z]\.$", before):  # an initial: J. Smith
            continue
        cuts.append(m.end())
    cuts.append(len(norm))
    for x, y in zip(cuts[:-1], cuts[1:], strict=True):
        if re.search(r"\w", norm[x:y]):
            out.append(
                Unit(a + idx[x], a + idx[min(y, len(idx) - 1)], pa, pb, "sentence")
            )


def units(p: Part, start: int = 0, end: int | None = None) -> list[Unit]:
    """Sentences, table cells and captions of p between two raw offsets (code excluded).

    A caption (``<figcaption>``, ``<p class="caption">``, an include's ``caption``, or a
    ``**Figure N.**`` paragraph) is one unit; so is each table cell (B1's caveats.yaml)."""
    end = len(p.raw) if end is None else end
    vis = list(p.vis)
    for x, y in p.code:
        vis[x:y] = _blank("".join(vis[x:y]))
    vis = "".join(vis)
    abbrev = _abbrevs()
    caps = sorted(caption_spans(p.raw))
    out: list[Unit] = []
    for blk in re.finditer(r"(?s)(?:(?!\n[ \t]*\n).)+", vis[:end]):
        pa, pb = blk.span()
        if pb <= start or not re.search(r"\w", blk.group(0)):
            continue
        pa = max(pa, start)
        covered = []
        for x, y in caps:
            if x < pb and y > pa:
                x, y = max(x, pa), min(y, pb)
                out.append(Unit(x, y, pa, pb, "caption"))
                covered.append((x, y))
        off = pa
        for ln in vis[pa:pb].split("\n"):
            lo, hi = off, off + len(ln)
            off = hi + 1
            if re.match(r"^\s*\|", ln) and not any(x <= lo < y for x, y in covered):
                if re.fullmatch(r"\s*\|?[\s:|-]*", ln):
                    covered.append((lo, hi))
                    continue
                for c in re.finditer(r"(?:\\\||[^|])+", ln):
                    if re.search(r"\w", c.group(0)):
                        out.append(Unit(lo + c.start(), lo + c.end(), pa, pb, "cell"))
                covered.append((lo, hi))
        pos = pa
        for x, y in sorted(covered) + [(pb, pb)]:
            if x > pos:
                _sentences(p, pos, x, pa, pb, out, abbrev)
            pos = max(pos, y)
    return sorted(out, key=lambda u: u.a)


def unit_text(p: Part, a: int, b: int) -> tuple[str, str]:
    """(reader-visible text, comment-free source text) of a range, whitespace collapsed."""
    return (
        re.sub(r"\s+", " ", p.vis[a:b]).strip(),
        re.sub(r"\s+", " ", p.nocomment[a:b]).strip(),
    )


def _matches(rxs: list[re.Pattern], texts: tuple[str, str]) -> bool:
    return any(rx.search(t) for rx in rxs for t in texts)


def run_caveats(
    parts: list[Part], caveats: list[dict], scope: Scope | None = None
) -> dict:
    """B1's semantics (caveats.yaml header). An occurrence is one unit (sentence, table cell
    or caption) matching any of an entry's patterns, tried on the reader-visible text and
    on the comment-free source text. Per entry:

    - each ``home`` file holds at least 1 and at most ``max_home`` occurrences (an appendix
      home is scanned for that entry only);
    - each ``also`` file holds at most ``max_also``;
    - every other main-text file holds 0. A pointer ("see §6.3", a link to the home)
      does not restate the caveat, so it does not match; a match in a sentence that links
      to the home is still counted, and marked.

    ``label_required`` entries: every main-text unit matching a ``trigger`` has a ``label``
    match in the same unit or the same paragraph.
    """
    scope = scope or Scope()
    by_name = {p.name: p for p in parts}
    main = [
        p
        for p in parts
        if main_text_offsets(p) > 0
        and (scope.main_files is None or p.name in scope.main_files)
    ]
    cache: dict[tuple[str, int, int], list[Unit]] = {}

    def get_units(p: Part, whole: bool) -> list[Unit]:
        end = len(p.raw) if whole else main_text_offsets(p)
        key = (p.name, 0, end)
        if key not in cache:
            cache[key] = units(p, 0, end)
        return cache[key]

    results = []
    for cv in caveats:
        rec = {
            "id": cv["id"],
            "name": cv.get("name", ""),
            "kind": cv["kind"],
            "occurrences": {},
            "violations": [],
            "problems": [],
        }
        if cv["kind"] == "label_required":
            for p in main:
                for u in get_units(p, False):
                    t = unit_text(p, u.a, u.b)
                    if not _matches(cv["trigger"], t):
                        continue
                    rec["occurrences"][p.name] = rec["occurrences"].get(p.name, 0) + 1
                    if not (
                        _matches(cv["label"], t)
                        or _matches(cv["label"], unit_text(p, u.pa, u.pb))
                    ):
                        rec["violations"].append(
                            {
                                "where": f"{p.name}:{p.line_of(u.a)}",
                                "why": "no label in the sentence or paragraph",
                                "text": t[0][:300],
                            }
                        )
            rec["status"] = "FAIL" if rec["violations"] else "PASS"
            results.append(rec)
            continue
        rec.update(home=cv["home"], also=cv["also"], patterns=cv["patterns"])
        ids = set()
        for h in cv["home"]:
            if h in by_name:
                ids |= heading_ids(by_name[h].raw)
            else:
                rec["problems"].append(f"home {h} is not a section file")
        scan = list(main) + [
            by_name[h] for h in cv["home"] if h in by_name and by_name[h] not in main
        ]
        for p in scan:
            whole = p.name in cv["home"]
            for u in get_units(p, whole):
                t = unit_text(p, u.a, u.b)
                if not _matches(cv["rxs"], t):
                    continue
                rec["occurrences"][p.name] = rec["occurrences"].get(p.name, 0) + 1
                n = rec["occurrences"][p.name]
                hit = {
                    "where": f"{p.name}:{p.line_of(u.a)}",
                    "unit": u.kind,
                    "text": t[0][:300],
                }
                links = {
                    x or y
                    for x, y in re.findall(
                        r"\]\(#([^)\s]+)\)|href=\"#([^\"]+)\"", p.raw[u.pa : u.pb]
                    )
                }
                if links & ids:
                    hit["links_to_home"] = sorted(links & ids)
                if whole:
                    if n > cv["max_home"]:
                        rec["violations"].append(
                            {
                                **hit,
                                "why": f"home holds more than max_home {cv['max_home']}",
                            }
                        )
                elif p.name in cv["also"]:
                    if n > cv["max_also"]:
                        rec["violations"].append(
                            {
                                **hit,
                                "why": f"more than max_also {cv['max_also']} in an also file",
                            }
                        )
                else:
                    rec["violations"].append({**hit, "why": "outside its home"})
        for h in cv["home"]:
            if h in by_name and not rec["occurrences"].get(h):
                rec["problems"].append(f"not stated in its home {h}")
        rec["status"] = (
            "PASS" if not rec["violations"] and not rec["problems"] else "FAIL"
        )
        results.append(rec)
    n_fail = sum(1 for r in results if r["status"] == "FAIL")
    return {
        "caveats": results,
        "failing": n_fail,
        "scope": scope.source,
        "scanned_main_text_files": [p.name for p in main],
        "unlisted_files": unlisted_files(parts, scope),
        "status": "PASS"
        if results and not n_fail
        else ("FAIL" if results else "EMPTY"),
    }


# ------------------------------------------------------------------ pages


@dataclass
class PdfLine:
    page: int
    y: float
    height: float
    text: str


def pdf_lines(pdf: Path) -> tuple[list[PdfLine], float, int]:
    out = subprocess.run(
        ["pdftotext", "-bbox-layout", str(pdf), "-"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    lines, page_h, n = [], 792.0, 0
    for pm in re.finditer(
        r'<page width="[\d.]+" height="([\d.]+)">(.*?)</page>', out, re.S
    ):
        n += 1
        page_h = float(pm.group(1))
        for lm in re.finditer(
            r'<line xMin="[\d.]+" yMin="([\d.]+)" xMax="[\d.]+" yMax="([\d.]+)">'
            r"(.*?)</line>",
            pm.group(2),
            re.S,
        ):
            words = [
                html.unescape(w)
                for w in re.findall(r"<word[^>]*>([^<]*)</word>", lm.group(3))
            ]
            y0, y1 = float(lm.group(1)), float(lm.group(2))
            lines.append(PdfLine(n, y0, y1 - y0, " ".join(words)))
    return lines, page_h, n


def norm_heading(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[‐-―]", "-", s)).strip().lower()


def find_heading(lines: list[PdfLine], name: str) -> list[dict]:
    """Every place the heading's text occupies one to three consecutive lines."""
    want = norm_heading(name)
    found = []
    for i, ln in enumerate(lines):
        acc, h = "", 0.0
        for j in range(i, min(i + 3, len(lines))):
            if lines[j].page != ln.page:
                break
            acc = (acc + " " + lines[j].text).strip()
            h = max(h, lines[j].height)
            got = norm_heading(acc)
            if got == want:
                found.append(
                    {
                        "page": ln.page,
                        "y": round(ln.y, 2),
                        "height": round(h, 2),
                        "lines": j - i + 1,
                    }
                )
                break
            if not want.startswith(got):
                break
    return found


def pick(found: list[dict]) -> dict | None:
    """The heading itself, not its table-of-contents entry: the tallest line; on a tie,
    the later one."""
    if not found:
        return None
    return max(found, key=lambda f: (round(f["height"], 1), f["page"], f["y"]))


def main_text_headings(parts: list[Part]) -> dict:
    """The H2 that ends the main text (the first H2 of the appendix) and the first
    numbered H2, read from the source the way load_parts split it."""
    first_num, end = None, None
    for p in parts:
        if p.name == "front_matter.yaml":
            continue
        for m in re.finditer(r"(?m)^##[ \t]+(.*?)[ \t]*#*[ \t]*$", p.vis):
            if p.in_code(m.start()):
                continue
            name = m.group(1).strip()
            in_app = p.appendix or (p.limit is not None and m.start() >= p.limit)
            if in_app and end is None:
                end = name
            if not in_app and first_num is None and re.search(START_RE, name):
                first_num = name
    return {"end_heading": end, "start_heading": first_num}


def run_pages(
    pdf: Path,
    end_name: str | None,
    start_name: str | None,
    max_pages: float,
    grade: str,
) -> dict:
    """Main-text printed pages. Position of a heading = (page - 1) + y / page height, so a
    full page counts 1.00 and figures, captions and margins count with their section
    (P1/P2/P3's method). Readings: from the top of page 1 to ``end_name``, and from
    ``start_name`` to ``end_name``. ``grade`` picks the graded one."""
    lines, page_h, n_pages = pdf_lines(pdf)
    rec = {
        "pdf": rel(pdf),
        "pages_in_pdf": n_pages,
        "page_height_pt": page_h,
        "start_heading": start_name,
        "end_heading": end_name,
        "max_pages": max_pages,
        "grade": grade,
        "notes": [],
    }

    def pos(f):
        return (f["page"] - 1) + f["y"] / page_h

    end = pick(find_heading(lines, end_name)) if end_name else None
    if end is None:
        # No appendix heading: the main text runs to the kit's own end matter.
        tail = [
            f for nm in ("Footnotes", "References") for f in find_heading(lines, nm)
        ]
        end = (
            min(tail, key=lambda f: (f["page"], f["y"]))
            if tail
            else {"page": n_pages, "y": page_h, "height": 0, "lines": 0}
        )
        rec["notes"].append(
            "the appendix heading was not found in the PDF"
            + (
                f" (source heading {end_name!r})"
                if end_name
                else " (no appendix in the source)"
            )
            + "; the main text is taken to end at "
            + ("the kit's Footnotes/References" if tail else "the last page")
        )
    start = pick(find_heading(lines, start_name)) if start_name else None
    if start is None:
        rec["notes"].append(
            f"the first numbered H2 ({start_name!r}) was not found in the PDF; the "
            "section-1 reading is not available"
        )
    rec["end"] = end
    rec["start"] = start
    rec["from_page1"] = round(pos(end), 3)
    rec["from_section1"] = round(pos(end) - pos(start), 3) if start else None
    graded = rec["from_page1"] if grade == "page1" else rec["from_section1"]
    rec["graded_pages"] = graded
    rec["status"] = "FAIL" if graded is None or graded > max_pages else "PASS"
    return rec


# ------------------------------------------------------------- legibility


def pdf_images(pdf: Path) -> list[dict]:
    out = subprocess.run(
        ["pdfimages", "-list", str(pdf)], capture_output=True, text=True, check=True
    ).stdout.splitlines()
    imgs = []
    for ln in out[2:]:
        c = ln.split()
        if len(c) < 14 or c[2] not in ("image",):
            continue
        imgs.append(
            {
                "page": int(c[0]),
                "w": int(c[3]),
                "h": int(c[4]),
                "xppi": float(c[12]),
                "yppi": float(c[13]),
            }
        )
    return imgs


def source_images(kit_source: str, files: dict) -> list[dict]:
    """Every image the kit source includes, in document order, with its source width."""
    from PIL import Image

    out = []
    for m in re.finditer(r"\{%\s*include\s+figure\.html\s+(.*?)%\}", kit_source, re.S):
        attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(1)))
        pub = attrs.get("path", "")
        src = files.get(pub)
        rec = {
            "path": pub,
            "file": src,
            "line": kit_source.count("\n", 0, m.start()) + 1,
        }
        fp = (ROOT / src) if src else None  # an absolute path stays absolute
        if fp is not None and fp.is_file():
            try:
                with Image.open(fp) as im:
                    rec["px"] = im.size
                    dpi = im.info.get("dpi")
                    rec["dpi"] = round(float(dpi[0]), 2) if dpi else None
            except OSError as e:
                rec["error"] = str(e)
        out.append(rec)
    return out


def run_legibility(
    pdf: Path,
    kit_source: str,
    files: dict,
    label_pt: float,
    min_pt: float,
    appendix_page: int | None = None,
) -> dict:
    imgs = pdf_images(pdf)
    srcs = source_images(kit_source, files)
    rows, j = [], 0
    for im in imgs:
        ar = im["h"] / im["w"]
        # match in document order: the next source image whose aspect ratio agrees
        k = j
        while k < len(srcs) and not (
            srcs[k].get("px")
            and abs(srcs[k]["px"][1] / srcs[k]["px"][0] - ar) <= 2.5 / im["w"] + 0.003
        ):
            k += 1
        row = {
            "pdf_page": im["page"],
            "pdf_px": [im["w"], im["h"]],
            "xppi": im["xppi"],
            "printed_in": round(im["w"] / im["xppi"], 2),
        }
        if appendix_page is not None:
            row["part"] = "appendix" if im["page"] >= appendix_page else "main"
        if k == len(srcs):
            row["status"] = "UNMATCHED"
            row["why"] = (
                "no included source image with this aspect ratio after the previous match"
            )
            rows.append(row)
            continue
        s = srcs[k]
        j = k + 1
        row.update(source=s["file"], source_line=s["line"])
        if not s.get("dpi"):
            row["status"] = "UNKNOWN"
            row["why"] = (
                "the source image records no dpi, so its drawn width is unknown"
            )
            rows.append(row)
            continue
        src_in = s["px"][0] / s["dpi"]
        scale = row["printed_in"] / src_in
        row.update(
            source_in=round(src_in, 2),
            scale=round(scale, 3),
            label_pt_printed=round(label_pt * scale, 2),
        )
        row["status"] = "PASS" if label_pt * scale >= min_pt else "FAIL"
        rows.append(row)
    bad = [r for r in rows if r["status"] in ("FAIL", "UNMATCHED", "UNKNOWN")]
    return {
        "pdf": rel(pdf),
        "label_pt": label_pt,
        "min_pt": min_pt,
        "images": rows,
        "failing": len(bad),
        "status": "PASS" if rows and not bad else ("FAIL" if rows else "EMPTY"),
    }


# ------------------------------------------------------- entry points


def resolve_scope(caveats_path: Path | None, appendix_re: str = APPENDIX_RE) -> Scope:
    return scope_from_map(
        caveats_path if caveats_path is not None else default_list("caveats"),
        appendix_re,
    )


def terms_check(
    root: Path,
    path: Path,
    registered: Path | None = None,
    parts: list[Part] | None = None,
    scope: Scope | None = None,
) -> dict:
    scope = scope or resolve_scope(None)
    parts = parts if parts is not None else load_parts(root, scope=scope)
    terms, problems = parse_terms(path)
    reg = registered or default_list("registered")
    res = run_terms(parts, terms, read_registered(reg))
    res.update(
        list=rel(path),
        registered_list=rel(reg) if reg else None,
        problems=problems,
        scope=scope.source,
        unlisted_files=unlisted_files(parts, scope),
    )
    if problems or not terms:
        res["status"] = "FAIL"
    return res


def dates_check(
    root: Path,
    path: Path | None,
    parts: list[Part] | None = None,
    scope: Scope | None = None,
    context_years: list[str] | None = None,
) -> dict:
    scope = scope or resolve_scope(None)
    parts = parts if parts is not None else load_parts(root, scope=scope)
    keys, rxs = parse_allow(path)
    res = run_dates(parts, keys, rxs, context_years)
    res.update(list=rel(path) if path else None, scope=scope.source)
    return res


def caveats_check(
    root: Path,
    path: Path | None,
    parts: list[Part] | None = None,
    scope: Scope | None = None,
) -> dict:
    if path is None or not Path(path).exists():
        return {
            "status": "NOT CONFIGURED",
            "list": rel(DEFAULTS["caveats"][0]),
            "caveats": [],
            "problems": [],
            "failing": 0,
        }
    scope = scope or scope_from_map(path)
    parts = parts if parts is not None else load_parts(root, scope=scope)
    cvs, problems = parse_caveats(path)
    res = run_caveats(parts, cvs, scope)
    res.update(list=rel(path), problems=problems)
    if problems:
        res["status"] = "FAIL"
    return res


def source_checks(
    root: Path,
    sections: list[tuple[str, str]] | None = None,
    front_matter: dict | None = None,
    terms: Path | None = None,
    registered: Path | None = None,
    allow: Path | None = None,
    caveats: Path | None = None,
    appendix_re: str = APPENDIX_RE,
) -> dict:
    """All three source-side checks on one reading of the paper (what build_v3.py runs)."""
    terms = terms or default_list("terms")
    allow = allow or default_list("dates")
    caveats = caveats or default_list("caveats")
    scope = resolve_scope(caveats, appendix_re)
    parts = load_parts(root, sections, scope=scope, front_matter=front_matter)
    out = {
        "scope": scope.source,
        "main_text": [
            p.name + ("" if p.limit is None else f" (to line {p.line_of(p.limit) - 1})")
            for p in parts
            if main_text_offsets(p) > 0
        ],
        "unlisted_files": unlisted_files(parts, scope),
        **main_text_headings(parts),
    }
    out["terms"] = (
        terms_check(root, terms, registered, parts, scope)
        if terms
        else {"status": "NOT CONFIGURED"}
    )
    out["dates"] = dates_check(root, allow, parts, scope)
    out["caveats"] = caveats_check(root, caveats, parts, scope)
    return out


def summary_lines(sc: dict, n: int = 12) -> list[str]:
    """Console lines for build_v3.py and the CLI."""
    out = [f"main text: {', '.join(sc['main_text']) or 'none'} (scope: {sc['scope']})"]
    if sc.get("unlisted_files"):
        out.append(
            f"  files in neither list of the one-home map: {sc['unlisted_files']}"
        )
    t = sc["terms"]
    if t["status"] == "NOT CONFIGURED":
        out.append("terms: NOT CONFIGURED")
    else:
        out.append(
            f"terms {t['status']}: {len(t['hits'])} hits ({t['list']}, {t['terms']} terms); "
            f"{len(t['exempt_registered'])} registered-exempt, {len(t['glossed'])} glossed, "
            f"{len(t['in_code_not_graded'])} in listings (not graded)"
        )
        out += [f"  {h['where']} {h['match']!r}: {h['context']}" for h in t["hits"][:n]]
        out += [f"  parse: {x}" for x in t.get("problems", [])]
    d = sc["dates"]
    out.append(
        f"dates {d['status']}: {len(d['hits'])} outside the allow-list ({d['list']}); "
        f"{len(d['allowed'])} allowed"
    )
    out += [f"  {h['where']} {h['match']!r}" for h in d["hits"][:n]]
    c = sc["caveats"]
    if c["status"] == "NOT CONFIGURED":
        out.append(f"caveats: NOT CONFIGURED ({c['list']} does not exist)")
    else:
        out.append(
            f"caveats {c['status']}: {c['failing']} of {len(c['caveats'])} entries fail ({c['list']})"
        )
        for r in c["caveats"]:
            if r["status"] == "FAIL":
                out.append(
                    f"  {r['id']} {r.get('name', '')}: "
                    + "; ".join(
                        r["problems"]
                        + [f"{v['where']} {v['why']}" for v in r["violations"][:3]]
                    )
                )
        out += [f"  parse: {x}" for x in c.get("problems", [])]
    return out


# ------------------------------------------------------------------- CLI


def _emit(res: dict, args, title: str, lines: list[str]) -> None:
    if getattr(args, "json", None):
        Path(args.json).write_text(
            json.dumps(res, indent=1, ensure_ascii=False, default=str) + "\n",
            encoding="utf-8",
        )
    print(f"{title}: {res['status']}")
    for ln in lines:
        print("  " + ln)
    sys.exit(1 if res["status"] == "FAIL" else 0)


def cli() -> None:
    ap = argparse.ArgumentParser(
        description="v3 main-text checks (see the module docstring)."
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p, root=True):
        if root:
            p.add_argument(
                "--root",
                type=Path,
                default=V3,
                help="paper folder with sections/ (and front_matter.yaml)",
            )
            p.add_argument(
                "--appendix-re",
                default=APPENDIX_RE,
                help="the first H2 matching this regex starts the appendix",
            )
            p.add_argument(
                "--scope-map",
                type=Path,
                default=None,
                help="one-home map whose main_text_files/appendix_files define the "
                "main text (default: the caveats map in use)",
            )
        p.add_argument("--json", type=Path, help="write the full result here")
        p.add_argument("--max-list", type=int, default=40, help="hits to print")

    p = sub.add_parser("terms")
    common(p)
    p.add_argument("--terms", type=Path, default=None)
    p.add_argument("--registered", type=Path, default=None)
    p = sub.add_parser("dates")
    common(p)
    p.add_argument("--allow", type=Path, default=None)
    p.add_argument(
        "--context-years",
        default=",".join(CONTEXT_YEARS),
        help="years that count as dates after a date word ('in 2026')",
    )
    p = sub.add_parser("caveats")
    common(p)
    p.add_argument("--caveats", type=Path, default=None)
    p = sub.add_parser("pages")
    common(p)
    p.add_argument("--pdf", type=Path, required=True)
    p.add_argument("--max-pages", type=float, default=15.0)
    p.add_argument(
        "--grade",
        choices=["page1", "section1"],
        default="page1",
        help="graded reading: from the top of page 1, or from the first numbered H2",
    )
    p.add_argument(
        "--end-heading", default=None, help="override: the H2 that ends the main text"
    )
    p.add_argument(
        "--start-heading", default=None, help="override: the first numbered H2"
    )
    p = sub.add_parser("legibility")
    common(p, root=False)
    p.add_argument("--pdf", type=Path, required=True)
    p.add_argument("--kit-source", type=Path, required=True)
    p.add_argument("--files", type=Path, required=True)
    p.add_argument("--label-pt", type=float, default=8.0)
    p.add_argument("--min-pt", type=float, default=7.0)
    args = ap.parse_args()
    n = args.max_list
    if args.cmd != "legibility":
        map_path = (
            args.scope_map or getattr(args, "caveats", None) or default_list("caveats")
        )
        scope = scope_from_map(map_path, args.appendix_re)

    if args.cmd == "terms":
        path = args.terms or default_list("terms")
        if path is None:
            _emit({"status": "NOT CONFIGURED"}, args, "terms", ["no term list"])
        res = terms_check(args.root, path, args.registered, scope=scope)
        out = [
            f"list {res['list']}: {res['terms']} terms; registered strings "
            f"{res['registered_list']} ({res['registered']}); scope {res['scope']}"
            + (f"; {len(res['problems'])} parse problems" if res["problems"] else ""),
            f"{len(res['hits'])} hits in the main text; {len(res['exempt_registered'])} exempt "
            f"(registered strings); {len(res['glossed'])} in a figure-label gloss; "
            f"{len(res['in_code_not_graded'])} in listings (not graded)",
            "per term: "
            + (", ".join(f"{k} {v}" for k, v in res["per_term"].items()) or "none"),
        ]
        out += [f"{h['where']} {h['term']}: {h['context']}" for h in res["hits"][:n]]
        out += [f"parse: {x}" for x in res["problems"]]
        _emit(res, args, "terms", out)
    if args.cmd == "dates":
        path = args.allow or default_list("dates")
        res = dates_check(
            args.root,
            path,
            scope=scope,
            context_years=[
                y.strip() for y in args.context_years.split(",") if y.strip()
            ],
        )
        out = [
            f"allow-list {res['list']}: {res['allow']}; scope {res['scope']}",
            f"{len(res['hits'])} dates outside the allow-list in the main text; "
            f"{len(res['allowed'])} allowed; {len(res['in_code_not_graded'])} in listings and "
            f"{len(res['bare_years_not_graded'])} other bare years (listed, not graded)",
        ]
        out += [
            f"{h['where']} [{h['kind']}, {h['in']}] {h['date']}: {h['context']}"
            for h in res["hits"][:n]
        ]
        _emit(res, args, "dates", out)
    if args.cmd == "caveats":
        path = args.caveats or default_list("caveats")
        if path is None or not path.exists():
            _emit(
                {"status": "NOT CONFIGURED"},
                args,
                "caveats",
                [f"no one-home map ({rel(DEFAULTS['caveats'][0])} does not exist)"],
            )
        res = caveats_check(args.root, path, scope=scope)
        problems = res["problems"]
        out = [
            f"map {res['list']}: {len(res['caveats'])} entries, {res['failing']} failing; "
            f"scope {res['scope']}; main-text files scanned {res['scanned_main_text_files']}"
            + (f"; {len(problems)} parse problems" if problems else "")
        ]
        if res["unlisted_files"]:
            out.append(f"files in neither list of the map: {res['unlisted_files']}")
        for c in res["caveats"]:
            occ = ", ".join(f"{k} {v}" for k, v in c["occurrences"].items()) or "none"
            head = (
                f"home {', '.join(c['home'])}; "
                if c["kind"] != "label_required"
                else "label_required; "
            )
            out.append(
                f"{c['status']} {c['id']} {c.get('name', '')}: {head}occurrences: {occ}"
                + (f"; {'; '.join(c['problems'])}" if c["problems"] else "")
            )
            out += [
                f"    {v['where']} ({v['why']}): {v['text'][:200]}"
                for v in c["violations"][:n]
            ]
        out += [f"parse: {x}" for x in problems]
        _emit(res, args, "caveats", out)
    if args.cmd == "pages":
        heads = main_text_headings(load_parts(args.root, scope=scope))
        end_name = args.end_heading or heads["end_heading"]
        start_name = args.start_heading or heads["start_heading"]
        res = run_pages(args.pdf, end_name, start_name, args.max_pages, args.grade)
        out = [
            f"{res['pdf']}: {res['pages_in_pdf']} pages; end heading {res['end_heading']!r} at "
            f"{res['end']}; first numbered H2 {res['start_heading']!r} at {res['start']}",
            f"main text from page 1: {res['from_page1']} pages; from section 1: "
            f"{res['from_section1']} pages; graded ({args.grade}) {res['graded_pages']} "
            f"against a ceiling of {args.max_pages:g}",
        ] + res["notes"]
        _emit(res, args, "pages", out)
    if args.cmd == "legibility":
        res = run_legibility(
            args.pdf,
            args.kit_source.read_text(encoding="utf-8"),
            json.loads(args.files.read_text(encoding="utf-8")),
            args.label_pt,
            args.min_pt,
        )
        out = [
            f"{len(res['images'])} printed images; a {args.label_pt:g} pt label must print at "
            f">= {args.min_pt:g} pt; {res['failing']} fail"
        ]
        for r in res["images"]:
            out.append(
                f"{r['status']} p{r['pdf_page']} {Path(r.get('source') or '?').name}: printed "
                f"{r['printed_in']} in, drawn {r.get('source_in', '?')} in -> "
                f"{r.get('label_pt_printed', '?')} pt"
                + (f" ({r['why']})" if r.get("why") else "")
            )
        _emit(res, args, "legibility", out)


if __name__ == "__main__":
    cli()
