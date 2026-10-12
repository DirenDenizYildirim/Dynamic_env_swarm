"""Build the Paper v2 kit source, an owner-facing preview, and a build report.

Implements the contract in ``paper/v2/INTERFACE.md``. Reads
``<root>/front_matter.yaml`` and ``<root>/sections/*.md`` (``root`` is ``paper/v2``
unless ``--root`` says otherwise), never ``paper/finale.md``, and writes:

- ``<root>/out/submission_v2.md``  the kit source: what ``submission_folder/submission.md``
  holds before comment stripping (YAML header with a generated ``toc`` and ``_styles``,
  then the sections in filename order). The repository copy keeps every comment;
  ``kit_stage.py`` strips them when it stages the upload (M4).
- ``<root>/out/index.html``        a preview in the kit's Distill look, with ledger IDs,
  comments and STUB-SPEC blocks on demand, each section's source beside it, and the
  build findings at the top. It is NOT the kit: kramdown's table and math rules are not
  emulated (the M1 scan below flags what the kit would turn into a table), and its
  reference list is a labelled emulation (a Python port of the kit's Distill code).
  ``kit_build.sh`` builds the real page.
- ``<root>/out/files.json``        published asset path -> repository file.
- ``<root>/out/build_report.json`` and ``<root>/out/crossrefs.md``  everything the build
  checked, for the review lanes and for ``kit_build.sh``.

The build FAILS (exit 1) on: a wrong line-1 status comment; an unresolved ledger ID; a
cite key not in the v2 bib; a listing whose fence body is not byte-identical to its
committed file lines (or a fence with no LISTING marker); Liquid other than the kit's two
forms; an unresolvable asset; a front-matter error; a ``toc`` name whose Jekyll slug is
not its heading's kramdown id. With ``--final`` it also fails on any M1 flag, a remaining
STUB-SPEC block, an unresolved cross-reference, a placeholder front-matter field, and any
warning.

Run from anywhere (pyyaml, markdown-it-py and pygments; the session's build venv has
them pinned to uv.lock):

    python paper/v2/src/build_v2.py [--root DIR] [--bib FILE] [--alt VARIANT]... [--final]
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from markdown_it import MarkdownIt
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

sys.dont_write_bytecode = True  # keep src/ free of __pycache__
sys.path.insert(0, str(Path(__file__).resolve().parent))
import distill_port as dp  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
V2 = ROOT / "paper" / "v2"
SRC = V2 / "src"
CANON_LEDGER = ROOT / "paper" / "numbers_ledger.md"
STATUS_LINE = ("<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): "
               "builder-drafted, not owner-approved -->")
ID_RE = r"[A-Z]+\d*-?\d+[a-z]?"
# Where each kit asset directory's files come from (basename lookup). A file under
# paper/v2/assets/<kind>/ wins; otherwise exactly one of the figure directories must hold it.
ASSET_DIRS = {
    "html": ["paper/figures/interactive/out/html", "paper/figures/out/html"],
    "img": ["paper/figures/interactive/out/img", "paper/figures/out/img",
            "paper/renders/2026-10-10/img"],
    "gif": ["paper/figures/out/gif", "paper/renders/2026-10-10/gif"],
}
BLOCK_TAGS = {"figure", "div", "details", "table", "p", "ul", "ol", "blockquote", "aside",
              "section", "pre", "iframe", "dl", "summary", "hr", "h1", "h2", "h3", "h4",
              "h5", "h6", "d-figure", "d-contents", "center"}
INCLUDE_ATTRS = {"path", "class", "alt", "caption", "style", "width", "height", "title",
                 "zoomable", "min-width", "min-height", "max-width", "max-height"}
DISTILL_MONTHS = ["Jan.", "Feb.", "March", "April", "May", "June", "July", "Aug.",
                  "Sept.", "Oct.", "Nov.", "Dec."]


# ---------------------------------------------------------------- records


@dataclass
class Report:
    failures: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    final_failures: list = field(default_factory=list)   # fail only with --final
    data: dict = field(default_factory=dict)

    def fail(self, where: str, msg: str) -> None:
        self.failures.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")

    def final(self, where: str, msg: str) -> None:
        self.final_failures.append(f"{where}: {msg}")


@dataclass
class Section:
    name: str          # published name, e.g. 03_environment.md
    path: Path         # the file actually read (may be an alt)
    raw: str
    html: str = ""
    m1_lines: list = field(default_factory=list)


def rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(ROOT))
    except ValueError:
        return p.name


# --------------------------------------------------------------- scanning


def mask_comments(text: str) -> str:
    """Replace every HTML comment by spaces, keeping newlines (so line numbers hold)."""
    return re.sub(r"<!--.*?-->", lambda m: re.sub(r"[^\n]", " ", m.group(0)), text, flags=re.S)


def fence_spans(lines: list[str]) -> list[tuple[int, int, str]]:
    """(open index, close index, info string) of each fenced code block (0-based)."""
    spans, i = [], 0
    while i < len(lines):
        m = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", lines[i])
        if m:
            fence = m.group(1)
            j = i + 1
            while j < len(lines) and not re.match(
                    rf"^ {{0,3}}{re.escape(fence[0])}{{{len(fence)},}}\s*$", lines[j]):
                j += 1
            spans.append((i, min(j, len(lines) - 1), m.group(2).strip()))
            i = j + 1
            continue
        i += 1
    return spans


def strip_code_spans(s: str) -> str:
    """Remove inline code spans (matching backtick runs), as kramdown protects them."""
    out, i = [], 0
    while i < len(s):
        if s[i] == "`":
            run = re.match(r"`+", s[i:]).group(0)
            j = s.find(run, i + len(run))
            while j != -1 and j + len(run) < len(s) and s[j + len(run)] == "`":
                j = s.find(run, j + len(run) + 1)
            if j == -1:
                out.append(s[i:i + len(run)])
                i += len(run)
                continue
            out.append(" " * (j + len(run) - i))
            i = j + len(run)
            continue
        out.append(s[i])
        i += 1
    return "".join(out)


LIQUID_REL = r"\{\{\s*'([^']+)'\s*\|\s*relative_url\s*\}\}"
LIQUID_INC = r"\{%\s*include\s+figure\.html\s+(.*?)%\}"


def classify_lines(text: str) -> tuple[list[str], list[str]]:
    """Return (kind per line, comment-masked lines). Kinds: fence, html, table, blank,
    prose. kramdown checks block HTML before tables, so lines inside a block-level HTML
    element are safe from M1; fenced code is too."""
    masked = mask_comments(text).split("\n")
    kinds = ["prose"] * len(masked)
    for a, b, _ in fence_spans(masked):
        for k in range(a, b + 1):
            kinds[k] = "fence"
    depth, tag = 0, None
    for i, ln in enumerate(masked):
        if kinds[i] == "fence":
            continue
        if depth > 0:
            kinds[i] = "html"
            depth += len(re.findall(rf"<{tag}\b", ln, re.I)) - len(re.findall(rf"</{tag}\s*>", ln, re.I))
            continue
        m = re.match(r"^ {0,3}<([A-Za-z][\w-]*)\b", ln)
        if m and m.group(1).lower() in BLOCK_TAGS:
            tag = re.escape(m.group(1))
            kinds[i] = "html"
            depth = len(re.findall(rf"<{tag}\b", ln, re.I)) - len(re.findall(rf"</{tag}\s*>", ln, re.I))
            continue
        if not ln.strip():
            kinds[i] = "blank"
    delim = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{1,}:?\s*)*\|?\s*$")
    i = 0
    while i < len(masked) - 1:
        if kinds[i] == "prose" and "|" in masked[i] and kinds[i + 1] == "prose" \
                and delim.match(masked[i + 1]):
            j = i
            while j < len(masked) and kinds[j] == "prose" and "|" in masked[j]:
                kinds[j] = "table"
                j += 1
            i = j
            continue
        i += 1
    return kinds, masked


def unescaped_pipes(s: str) -> list[int]:
    return [m.start() for m in re.finditer(r"(?<!\\)\|", s)]


def table_cells(row: str) -> int:
    s = strip_code_spans(row).strip()
    s = s[1:] if s.startswith("|") else s
    s = s[:-1] if s.endswith("|") and not s.endswith("\\|") else s
    return len(unescaped_pipes(s)) + 1


def m1_scan(sec: Section, rep: Report) -> dict:
    """Source side of M1: every non-code, non-table, non-HTML line with an unescaped '|'
    (math included: kramdown's table check runs before math). Also table rows whose cell
    count differs from their header's (a pipe inside a cell, e.g. in math)."""
    kinds, masked = classify_lines(sec.raw)
    flags, md_tables, html_tables, in_display = [], 0, 0, False
    header_cells = None
    for i, ln in enumerate(masked):
        k = kinds[i]
        if k == "html":
            html_tables += len(re.findall(r"<table\b", ln, re.I))
            continue
        if k == "table":
            if i == 0 or kinds[i - 1] != "table":
                md_tables += 1
                header_cells = table_cells(ln)
            elif not re.match(r"^\s*\|?\s*:?-{3,}", ln):
                n = table_cells(ln)
                if n != header_cells:
                    flags.append({"line": i + 1, "kind": "table-cell",
                                  "text": sec.raw.split("\n")[i].strip()[:160],
                                  "why": f"{n} cells against the header's {header_cells}"})
            continue
        if k != "prose":
            continue
        s = re.sub(LIQUID_REL, "URL", ln)
        s = re.sub(LIQUID_INC, "INCLUDE", s)
        s = strip_code_spans(s)
        s = re.sub(r"^\s*(>\s*)+", "", s)
        if s.strip() == "$$":
            in_display = not in_display
        pipes = unescaped_pipes(s)
        if pipes:
            spans = [(m.start(), m.end()) for m in re.finditer(
                r"\$\$.+?\$\$|(?<![\\$])\$[^$\n]+?\$(?!\$)", s)]
            in_math = any(a <= p < b for p in pipes for a, b in spans)
            kind = "display-math" if in_display else "inline-math" if in_math else "prose"
            flags.append({"line": i + 1, "kind": kind,
                          "text": sec.raw.split("\n")[i].strip()[:160],
                          "why": f"{len(pipes)} unescaped '|' outside code"})
    for f in flags:
        f["section"] = sec.name
        rep.final(f"{sec.name}:{f['line']}", f"M1 [{f['kind']}] {f['why']}: {f['text'][:90]}")
    sec.m1_lines = [f["line"] for f in flags]
    return {"flags": flags, "md_tables": md_tables, "html_tables": html_tables}


def math_count(text: str) -> int:
    kinds, masked = classify_lines(text)
    n, in_disp = 0, False
    for i, ln in enumerate(masked):
        if kinds[i] not in ("prose", "table"):
            continue
        s = strip_code_spans(ln)
        if s.strip() == "$$":
            if in_disp:
                n += 1
            in_disp = not in_disp
            continue
        if in_disp:
            continue
        n += len(re.findall(r"\$\$.+?\$\$|(?<![\\$])\$[^$\n]+?\$(?!\$)", s))
    return n


# --------------------------------------------------------------- ledgers


def read_ledgers(root: Path) -> tuple[dict, list[Path]]:
    sources = [CANON_LEDGER, root / "ledger_supplement.md",
               *sorted((root / "ledger_proposals").glob("*.md"))]
    rows: dict[str, dict] = {}
    for path in sources:
        if not path.exists():
            continue
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 3 and re.fullmatch(ID_RE, cells[0]):
                rid = cells[0]
                entry = {"value": cells[1], "what": cells[2], "source": f"{rel(path)}:{n}"}
                if rid in rows and rows[rid]["value"] != entry["value"]:
                    rows[rid].setdefault("conflicts", []).append(entry["source"])
                rows.setdefault(rid, entry)
    return rows, [p for p in sources if p.exists()]


# ------------------------------------------------------------ front matter


def read_front_matter(root: Path, rep: Report) -> dict:
    path = root / "front_matter.yaml"
    if not path.exists():
        rep.fail("front_matter.yaml", "missing")
        return {}
    try:
        fm = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        rep.fail("front_matter.yaml", f"YAML error: {e}")
        return {}
    w = "front_matter.yaml"
    if fm.get("layout") != "distill":
        rep.fail(w, "layout must be distill")
    for key in ("title", "description"):
        v = fm.get(key)
        if not isinstance(v, str) or not v.strip():
            rep.fail(w, f"{key} missing")
            continue
        if "\n" in v:
            rep.fail(w, f"{key} must be one line (it is a JS string literal in distill.html)")
        for ch, why in (('"', "breaks the layout's JS string and JSON"),
                        ("\\", "is an escape in the layout's JS string")):
            if ch in v:
                rep.fail(w, f"{key} contains {ch!r}: {why}")
        for ch in "<>&":
            if ch in v:
                rep.warn(w, f"{key} contains {ch!r}, which the layout prints as raw HTML")
        if "{{" in v or "{%" in v:
            rep.fail(w, f"{key} contains Liquid")
        if v.strip().upper().startswith("PLACEHOLDER"):
            rep.final(w, f"{key} is still a placeholder")
    date = fm.get("date")
    if date is None:
        rep.warn(w, "no date: the kit's 'cite this work' box gets an empty year (M3)")
    elif not isinstance(date, (dt.date, dt.datetime)):
        rep.fail(w, f"date {date!r} is not a YAML date")
    elif (date.date() if isinstance(date, dt.datetime) else date) > dt.date.today():
        rep.warn(w, f"date {date} is in the future: Jekyll skips the page without --future")
    dc = fm.get("date_confirmed", False)
    if not isinstance(dc, bool):
        rep.fail(w, f"date_confirmed {dc!r} must be true or false")
    elif not dc:
        rep.final(w, "date is not confirmed by the owner (set date_confirmed: true once it "
                  "is; review RM-23)")
    sd = fm.get("submitted_date")
    if sd is not None and not isinstance(sd, (dt.date, dt.datetime)):
        rep.fail(w, f"submitted_date {sd!r} is not a YAML date")
    authors = fm.get("authors") or []
    if not authors:
        rep.fail(w, "authors missing")
    for a in authors:
        if not isinstance(a, dict) or a.get("name") != "Anonymous" or "url" in a \
                or (a.get("affiliations") or {}).get("name") != "Anonymous":
            rep.fail(w, f"author entry must be Anonymous, with no url: {a!r}")
    if fm.get("bibliography") != "submission.bib":
        rep.fail(w, "bibliography must be submission.bib")
    for bad in ("openreview_id", "toc", "_styles"):
        if bad in fm:
            rep.fail(w, f"{bad} must not be set here" +
                     (" (the build generates it)" if bad != "openreview_id" else
                      " during review (KIT_NOTES §S1.4)"))
    return fm


def yaml_scalar(s: str) -> str:
    return "'" + s.replace("'", "''") + "'"


def kit_date(d) -> str:
    return d.strftime("%Y-%m-%d") if isinstance(d, (dt.date, dt.datetime)) else str(d)


STYLES_FILE = SRC / "kit_styles.css"


def styles_line() -> str:
    css = STYLES_FILE.read_text(encoding="utf-8")
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    return re.sub(r"\s+", " ", css).strip()


# ------------------------------------------------------------ section checks


# Alternates that cannot be built by swapping one file (review RM-6). 00_hero.ladder.md is
# a caption draft for option B (STRUCTURE.md section 9), which also needs section 1's ladder
# block moved to the hero slot, the explorer moved to the head of section 3, Figures 1 and
# 3 swapped throughout and the duplicate removed. A plain swap builds an incoherent page.
NOT_BUILDABLE = {
    "00_hero.ladder.md": "a caption draft for hero option B only (STRUCTURE.md section 9): "
    "option B also moves section 1's ladder block to the hero slot and the explorer to the "
    "head of section 3, and swaps Figures 1 and 3 throughout. A plain file swap builds an "
    "incoherent page (review RM-6), so this build refuses it. Read the file as a draft.",
}


def load_sections(root: Path, alts: list[str], rep: Report) -> list[Section]:
    sdir = root / "sections"
    files = sorted(p for p in sdir.glob("*.md"))
    alt_dir = sdir / "alt"
    available = sorted(p.name for p in alt_dir.glob("*.md")) if alt_dir.exists() else []
    rep.data["alt_available"] = available
    chosen: dict[str, Path] = {}
    for spec in alts:
        if "." in spec:
            name, variant = spec.split(".", 1)
            cand = [alt_dir / f"{name}.{variant}.md"]
        else:
            cand = [alt_dir / a for a in available if a.split(".")[1] == spec]
        hits = [c for c in cand if c.exists()]
        if not hits:
            rep.fail("--alt", f"no alternate matches {spec!r} (available: {available})")
        for c in hits:
            if c.name in NOT_BUILDABLE:
                rep.fail(f"--alt {spec}", f"sections/alt/{c.name} is {NOT_BUILDABLE[c.name]}")
                continue
            chosen[c.name.split(".")[0] + ".md"] = c
    sections = []
    for p in files:
        use = chosen.pop(p.name, p)
        sections.append(Section(p.name, use, use.read_text(encoding="utf-8")))
    for name in chosen:
        rep.fail("--alt", f"alternate for {name}, which has no main file")
    rep.data["alt_used"] = {s.name: rel(s.path) for s in sections if s.path.parent.name == "alt"}
    names = [s.name for s in sections]
    if names[:2] != ["00_abstract.md", "00_hero.md"]:
        rep.fail("sections", f"the first two files must be 00_abstract.md, 00_hero.md; got {names[:2]}")
    for s in sections:
        first = s.raw.split("\n", 1)[0]
        if first != STATUS_LINE:
            rep.fail(f"{rel(s.path)}:1", "line 1 must be the exact PAPER V2 status comment")
    return sections


def committed_lines(path: str) -> tuple[list[str] | None, str]:
    """Lines of the file as committed at HEAD, and a note if the work tree differs."""
    try:
        blob = subprocess.run(["git", "-C", str(ROOT), "show", f"HEAD:{path}"],
                              capture_output=True, check=True).stdout.decode("utf-8")
    except subprocess.CalledProcessError:
        return None, "not committed at HEAD"
    note = ""
    wt = ROOT / path
    if wt.exists() and wt.read_text(encoding="utf-8") != blob:
        note = "work tree differs from HEAD"
    return blob.split("\n"), note


def check_listings(sec: Section, rep: Report) -> list[dict]:
    lines = sec.raw.split("\n")
    masked = mask_comments(sec.raw).split("\n")
    out = []
    for a, b, info in fence_spans(masked):
        where = f"{sec.name}:{a + 1}"
        j = a - 1
        while j >= 0 and not lines[j].strip():
            j -= 1
        m = re.match(r"^<!--\s*LISTING:\s*(\S+?):(\d+)-(\d+)\s*-->\s*$", lines[j]) if j >= 0 else None
        rec = {"section": sec.name, "line": a + 1, "info": info, "ok": False}
        out.append(rec)
        if not m:
            rep.fail(where, "fenced code with no '<!-- LISTING: path:start-end -->' line before it")
            continue
        path, start, end = m.group(1), int(m.group(2)), int(m.group(3))
        rec.update(path=path, start=start, end=end)
        body = lines[a + 1:b]
        header = re.match(r"^#\s*(\S+?):(\d+)-(\d+)\s*\(verbatim\)\s*$", body[0]) if body else None
        if header:
            rec["header"] = body[0]
            if (header.group(1), int(header.group(2)), int(header.group(3))) != (path, start, end):
                rep.fail(where, f"header line {body[0]!r} disagrees with the LISTING marker")
            body = body[1:]
        flines, note = committed_lines(path)
        if flines is None:
            rep.fail(where, f"{path}: {note}")
            continue
        if note:
            rep.warn(where, f"{path}: {note}; compared with HEAD")
        want = flines[start - 1:end]
        if body != want:
            diff = next((k for k in range(max(len(body), len(want)))
                         if k >= len(body) or k >= len(want) or body[k] != want[k]), None)
            rep.fail(where, f"listing differs from {path}:{start}-{end} "
                     f"(first difference at listing line {diff + 1 if diff is not None else '?'}; "
                     f"{len(body)} lines against {len(want)})")
            continue
        joined = "\n".join(lines[a + 1:b])
        if re.search(r"(?<![\\$])\$(?!\$)", joined) or "$$" in joined:
            rep.fail(where, "listing contains '$': the kit rewrites it to '$$' in code too")
            continue
        if "{{" in joined or "{%" in joined:
            rep.fail(where, "listing contains Liquid delimiters, which the kit executes")
            continue
        rec["ok"] = True
        rec["text"] = "\n".join(want)
        rec["max_len"] = max((len(x) for x in want), default=0)
    return out


def check_liquid(sec: Section, rep: Report, assets: set) -> dict:
    counts = {"include": 0, "relative_url": 0}
    text = sec.raw
    for m in re.finditer(r"\{\{.*?\}\}|\{%.*?%\}|\{\{|\{%", text, flags=re.S):
        tok = m.group(0)
        line = text[:m.start()].count("\n") + 1
        where = f"{sec.name}:{line}"
        r = re.fullmatch(LIQUID_REL, tok)
        inc = re.fullmatch(LIQUID_INC, tok, flags=re.S)
        if r:
            counts["relative_url"] += 1
            assets.add((r.group(1), where))
        elif inc:
            counts["include"] += 1
            attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', inc.group(1)))
            leftover = re.sub(r'([\w-]+)="([^"]*)"', "", inc.group(1)).strip()
            if leftover:
                rep.fail(where, f"include has unparsed text {leftover[:60]!r} (a stray quote?)")
            for k in attrs:
                if k not in INCLUDE_ATTRS:
                    rep.warn(where, f"include attribute {k!r} is not one figure.html reads")
            if "path" not in attrs:
                rep.fail(where, "include without path")
            else:
                assets.add((attrs["path"], where))
            if "$" in inc.group(1):
                rep.final(where, "'$' inside an include attribute (the kit rewrites it)")
        else:
            rep.fail(where, f"Liquid not in the kit's two forms: {tok[:70]!r}")
    return counts


def check_tags_and_cites(sec: Section, rep: Report, ledger: dict, bib: dict | None,
                         seen: dict) -> None:
    for m in re.finditer(r"<!--\s*N:(.*?)-->", sec.raw, flags=re.S):
        line = sec.raw[:m.start()].count("\n") + 1
        ids = [x for x in re.split(r"[,\s]+", m.group(1).strip()) if x]
        if not ids:
            rep.fail(f"{sec.name}:{line}", "empty ledger tag")
        for rid in ids:
            seen["ids"].setdefault(rid, []).append(f"{sec.name}:{line}")
            if not re.fullmatch(ID_RE, rid):
                rep.fail(f"{sec.name}:{line}", f"malformed ledger ID {rid!r}")
            elif rid not in ledger:
                rep.fail(f"{sec.name}:{line}", f"ledger ID {rid} resolves in no ledger source")
    for m in re.finditer(r"<d-cite\b[^>]*>", sec.raw):
        line = sec.raw[:m.start()].count("\n") + 1
        km = re.fullmatch(r'<d-cite key="([^"]+)">', m.group(0))
        close = sec.raw[m.end():m.end() + 9] == "</d-cite>"
        if not km or not close:
            rep.fail(f"{sec.name}:{line}", f"malformed citation {m.group(0)!r} "
                     "(write <d-cite key=\"k1,k2\"></d-cite>)")
            continue
        for key in [k.strip() for k in km.group(1).split(",")]:
            seen["cites"].append(key)
            if bib is not None and key not in bib:
                rep.fail(f"{sec.name}:{line}", f"cite key {key!r} is not in the v2 bib")


def check_footnotes_and_html(sec: Section, rep: Report, notes: list) -> None:
    for m in re.finditer(r"<d-footnote>(.*?)</d-footnote>", sec.raw, flags=re.S):
        line = sec.raw[:m.start()].count("\n") + 1
        body = m.group(1)
        notes.append({"section": sec.name, "line": line,
                      "text": re.sub(r"<!--.*?-->", "", body, flags=re.S).strip()})
        for pat, why in ((r"\$", "math ('$')"), (r"<d-cite", "a citation"), ('"', "a double quote")):
            if re.search(pat, body):
                rep.warn(f"{sec.name}:{line}", f"<d-footnote> contains {why} (P2 §7.4)")
    kinds, masked = classify_lines(sec.raw)
    for i, ln in enumerate(masked):
        if kinds[i] == "html" and "$" in ln:
            rep.final(f"{sec.name}:{i + 1}", "'$' inside raw HTML: kramdown leaves it, the kit "
                      "rewrites it to '$$' and MathJax renders display math there; use Unicode")
        if kinds[i] in ("prose", "table"):
            s = strip_code_spans(ln)
            if re.match(r"^\s{0,3}(\{:|\*\[|\[\^|: )", s):
                rep.warn(f"{sec.name}:{i + 1}", "line starts a kramdown extension "
                         "(attribute list, abbreviation, footnote or definition list)")
            if re.fullmatch(r"\s*\$[^$]+\$\s*", s):
                rep.warn(f"{sec.name}:{i + 1}", "a lone inline math paragraph becomes display "
                         "math after the kit's $ -> $$ rewrite")
            if re.search(r"<br\s*/?>", s, re.I):
                rep.warn(f"{sec.name}:{i + 1}", "<br> in prose")
    for m in re.finditer(r"<!--(.*?)-->", sec.raw, flags=re.S):
        if "<!--" in m.group(1):
            line = sec.raw[:m.start()].count("\n") + 1
            rep.fail(f"{sec.name}:{line}", "a comment contains '<!--': comments do not nest, so "
                     "the first '-->' ends it and the rest would show on the page")
    if "-->" in re.sub(r"<!--.*?-->", "", sec.raw, flags=re.S) or \
            "<!--" in re.sub(r"<!--.*?-->", "", sec.raw, flags=re.S):
        rep.fail(sec.name, "an unmatched '<!--' or '-->' (its text would show on the page)")
    for i, ln in enumerate(masked):
        if kinds[i] in ("prose", "table", "html") and "<!--" in sec.raw.split("\n")[i]:
            raw_line = sec.raw.split("\n")[i]
            for cm in re.finditer(r"(`+)(.+?)\1", raw_line):
                if "<!--" in cm.group(2):
                    rep.warn(f"{sec.name}:{i + 1}", "an HTML comment inside inline code: staging "
                             "strips it, so the shown code would change")
    for m in re.finditer(r"<!--(.*?)-->", sec.raw, flags=re.S):
        if "--" in m.group(1).strip("-"):
            line = sec.raw[:m.start()].count("\n") + 1
            rep.warn(f"{sec.name}:{line}", "'--' inside an HTML comment (invalid comment syntax)")


# ------------------------------------------------------------ cross-references

REF_PATTERNS = [
    ("section", r"§\s?(\d+(?:\.\d+)*)"),
    ("section", r"\bSections?\s+(\d+(?:\.\d+)*)"),
    ("figure", r"\bFig(?:ure|\.)s?\s+([A-Z]?\d+)"),
    ("table", r"\bTables?\s+([A-Z]?\d+)"),
    ("listing", r"\bListings?\s+(\d+)"),
    ("appendix", r"\bApp(?:endix|endices|\.)\s+([A-Z])\b"),
    ("definition", r"\bDefinitions?\s+(\d+)"),
    ("proposition", r"\bPropositions?\s+(\d+)"),
    ("theorem", r"\bTheorems?\s+(\d+)"),
    ("corollary", r"\bCorollar(?:y|ies)\s+(\d+)"),
    ("remark", r"\bRemarks?\s+(\d+[′″']*)"),
]
# More labels of the same kind after the first ("Figures 2 and 3", "§5–6", "§5 and §6").
# A tail never crosses into another kind: "(Figure 2, §1)" is Figure 2 and §1, and a
# section tail needs "§" after a comma or "and" ("§9.2, 4.83-fold" is §9.2 only).
RANGE_TAIL = r"((?:\s*(?:,|and|–|-|to|or)\s*[A-Z]?\d+(?:\.\d+)*\b(?![.\d]*\s*[-–]?fold))*)"
SECTION_TAIL = (r"((?:\s*(?:–|-|to)\s*(?:§\s?)?\d+(?:\.\d+)*\b"
                r"|\s*(?:,|and|or)\s*§\s?\d+(?:\.\d+)*\b)*)")
# What may stand between "their" (or a possessive) and a reference that is then
# taken to number a cited work: other reference words, numbers and joiners only.
EXT_TAIL = (r"(?:(?:Tables?|Theorems?|Figures?|Fig\.|Sections?|§|Propositions?|Lemmas?|"
            r"Corollar(?:y|ies)|Definitions?|Remarks?|Listings?|Appendix|Eqs?\.|and|or|,|–|-|"
            r"[A-Z]?\d+(?:\.\d+)*)\s*)*")


def collect_targets(sections: list[Section]) -> dict:
    targets: dict[tuple[str, str], dict] = {}
    in_appendix = False

    def add(kind, label, sec, line, text):
        targets.setdefault((kind, label), {"where": f"{sec.name}:{line}", "text": text[:90]})

    for sec in sections:
        kinds, masked = classify_lines(sec.raw)
        for i, ln in enumerate(masked):
            if kinds[i] == "fence":
                continue
            h2 = re.match(r"^##\s+(.*\S)\s*$", ln)
            h3 = re.match(r"^###\s+(.*\S)\s*$", ln)
            if h2:
                t = h2.group(1)
                in_appendix = bool(re.match(r"^Appendi", t))
                if (m := re.match(r"^(\d+)\s", t)):
                    add("section", m.group(1), sec, i + 1, t)
                if (m := re.match(r"^Appendix\s+([A-Z])\b", t)):
                    add("appendix", m.group(1), sec, i + 1, t)
            elif h3:
                t = h3.group(1)
                if (m := re.match(r"^(\d+\.\d+)\s", t)):
                    add("section", m.group(1), sec, i + 1, t)
                elif in_appendix and (m := re.match(r"^([A-Z])\s", t)):
                    add("appendix", m.group(1), sec, i + 1, t)
            for kind, word in (("figure", "Figure"), ("table", "Table"), ("listing", "Listing")):
                for m in re.finditer(rf"(?:<strong>|\*\*|caption=\"){word}\s+([A-Z]?\d+)\.", ln):
                    add(kind, m.group(1), sec, i + 1, ln.strip())
            for kind, word in (("definition", "Definition"), ("proposition", "Proposition"),
                               ("theorem", "Theorem"), ("corollary", "Corollary"),
                               ("remark", "Remark")):
                for m in re.finditer(rf"(?:<strong>|\*\*){word}\s+(\d+[′″']*)", ln):
                    add(kind, m.group(1), sec, i + 1, ln.strip())
    return targets


def collect_refs(sections: list[Section], targets: dict, rep: Report) -> list[dict]:
    refs = []
    for sec in sections:
        kinds, masked = classify_lines(sec.raw)
        for i, ln in enumerate(masked):
            if kinds[i] == "fence" or re.match(r"^#{2,3}\s", ln):
                continue
            s = strip_code_spans(ln)
            for kind, pat in REF_PATTERNS:
                for m in re.finditer(pat + (SECTION_TAIL if kind == "section" else RANGE_TAIL), s):
                    labels = [m.group(1)] + re.findall(r"[A-Z]?\d+(?:\.\d+)*", m.group(2) or "")
                    # "their Table 5", "Chen et al.'s Theorem 4": numbering of a cited work.
                    lead = s[:m.start()]
                    external = bool(re.search(r"(?:\btheir|['’]s)\s+" + EXT_TAIL + r"$", lead))
                    for lab in labels:
                        if external:
                            refs.append({"from": f"{sec.name}:{i + 1}", "kind": kind, "label": lab,
                                         "context": s.strip()[max(0, m.start() - 30):m.end() + 30],
                                         "target": "external", "target_text": "a cited work's own "
                                         "numbering ('their' or a possessive before it); not checked"})
                            continue
                        t = targets.get((kind, lab))
                        if t is None and kind == "section" and "." not in lab:
                            t = targets.get(("section", lab))
                        refs.append({"from": f"{sec.name}:{i + 1}", "kind": kind, "label": lab,
                                     "context": s.strip()[max(0, m.start() - 30):m.end() + 30],
                                     "target": t["where"] if t else None,
                                     "target_text": t["text"] if t else None})
                        if t is None:
                            rep.final(f"{sec.name}:{i + 1}", f"cross-reference {kind} {lab} "
                                      "resolves to no heading or caption")
    return refs


# ------------------------------------------------------------- assets


def resolve_assets(paths: set, rep: Report, root: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for p, where in sorted(paths):
        m = re.fullmatch(r"assets/(html|img|gif)/submission/([^/]+)", p)
        if not m:
            rep.fail(where, f"asset path outside the kit layout: {p}")
            continue
        own = root / "assets" / m.group(1) / m.group(2)
        if own.is_file():
            files[p] = rel(own)
            continue
        hits = [d for d in ASSET_DIRS[m.group(1)] if (ROOT / d / m.group(2)).is_file()]
        if len(hits) != 1:
            rep.fail(where, f"asset {p}: {len(hits)} candidate files ({hits})")
            continue
        files[p] = f"{hits[0]}/{m.group(2)}"
    return files


# --------------------------------------------------------- preview rendering


def _protect(pattern: str, text: str, store: list, tag: str, flags=0) -> str:
    def sub(m):
        store.append(m.group(0))
        return f"{tag}{len(store) - 1}Q"
    return re.sub(pattern, sub, text, flags=flags)


def _restore(text: str, store: list, tag: str) -> str:
    return re.sub(rf"{tag}(\d+)Q", lambda m: store[int(m.group(1))], text)


def comments_to_notes(text: str, ledger: dict) -> str:
    def chip(m):
        out = []
        for rid in [x for x in re.split(r"[,\s]+", m.group(1).strip()) if x]:
            row = ledger.get(rid)
            tip = f"{row['value']} — {row['what']} ({row['source']})" if row else "NOT IN LEDGER"
            out.append(f'<span class="note note-ledger" title="{html.escape(tip)}">{html.escape(rid)}</span>')
        return "".join(out)

    text = re.sub(r"<!--\s*N:(.*?)-->", chip, text, flags=re.S)

    def block(m):
        body = m.group(1).strip()
        if ("<!--" + m.group(1) + "-->").strip() == STATUS_LINE:
            return ""
        tag = "STUB-SPEC (stripped at staging)" if body.startswith("STUB-SPEC") else "hidden comment"
        return (f'\n<div class="note note-block"><span class="note-tag">{tag}</span>'
                f"{html.escape(body)}</div>\n")

    text = re.sub(r"^[ \t]*<!--(.*?)-->[ \t]*$", block, text, flags=re.S | re.M)
    return re.sub(r"<!--(.*?)-->", lambda m: f'<span class="note note-inline">'
                  f"{html.escape(m.group(1).strip())}</span>", text, flags=re.S)


def liquid_expand(text: str) -> str:
    text = re.sub(LIQUID_REL, lambda m: m.group(1), text)

    def include(m):
        attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(1)))
        cls = attrs.get("class", "")
        alt = html.escape(attrs.get("alt", ""), quote=True)
        style = f' style="{attrs["style"]}"' if "style" in attrs else ""
        cap = attrs.get("caption", "")
        cap_html = (f'<figcaption class="caption" style="text-align: center; width: 100%;">{cap}</figcaption>'
                    if cap else "")
        return (f'\n<figure style="text-align: center; width: 100%;"><picture>'
                f'<img src="{attrs.get("path", "")}" class="{cls}" alt="{alt}"{style} loading="lazy">'
                f"</picture>{cap_html}</figure>\n")

    return re.sub(LIQUID_INC, include, text, flags=re.S)


def protect_math(text: str, store: list) -> str:
    text = text.replace("\\$", "DOLLARQ")

    def disp(m):
        store.append(("display", m.group(1)))
        return f"\n\nMXQ{len(store) - 1}Q\n\n"

    text = re.sub(r"(?m)^[ \t]*\$\$(.+?)\$\$[ \t]*$", disp, text, flags=re.S | re.M)

    def inl(m):
        store.append(("inline", m.group(1) or m.group(2)))
        return f"MXQ{len(store) - 1}Q"

    return re.sub(r"\$\$(.+?)\$\$|(?<![\\\w])\$([^\s$](?:[^$\n]*?[^\s$])?)\$", inl, text)


def restore_math(text: str, store: list) -> str:
    def sub(m):
        kind, tex = store[int(m.group(1))]
        tex = html.escape(tex.strip(), quote=False)
        return f'<div class="math-display">\\[{tex}\\]</div>' if kind == "display" else f"\\({tex}\\)"
    text = re.sub(r"<p>MXQ(\d+)Q</p>", sub, text)
    return re.sub(r"MXQ(\d+)Q", sub, text).replace("DOLLARQ", "$")


def _highlight(code: str, lang: str, _attrs) -> str:
    try:
        lexer = get_lexer_by_name(lang or "text")
    except ClassNotFound:
        lexer = get_lexer_by_name("text")
    return highlight(code, lexer, HtmlFormatter(nowrap=True))


MD = MarkdownIt("commonmark", {"html": True, "highlight": _highlight})
MD.enable(["table", "strikethrough"])


def mark_m1(raw: str, lines: list[int]) -> str:
    out = raw.split("\n")
    for n in lines:
        out[n - 1] = re.sub(r"^(\s*(?:[-*+]\s+|\d+\.\s+|>\s*)*)",
                            lambda m: m.group(1) + '<span class="m1-flag" title="M1: the kit would '
                            'parse this line as a table row (unescaped |)">M1</span> ', out[n - 1],
                            count=1)
    return "\n".join(out)


def render_section(raw: str, ledger: dict, m1_lines: list[int]) -> str:
    text = mark_m1(raw, m1_lines)
    code: list = []
    text = _protect(r"(?ms)^ {0,3}(`{3,}|~{3,}).*?^ {0,3}\1[ \t]*$", text, code, "FNQ")
    text = _protect(r"`[^`\n]+`", text, code, "ICQ")
    text = comments_to_notes(text, ledger)
    text = liquid_expand(text)
    math: list = []
    text = protect_math(text, math)
    text = _restore(text, code, "ICQ")
    text = _restore(text, code, "FNQ")
    return restore_math(MD.render(text), math)


def add_heading_ids(body: str, counter: dict) -> str:
    def sub(m):
        level, inner = m.group(1), m.group(2)
        plain = html.unescape(re.sub(r"<[^>]+>", "", inner))
        sid = dp.kramdown_id(plain)
        counter[sid] = counter.get(sid, -1) + 1
        if counter[sid]:
            sid = f"{sid}-{counter[sid]}"
        return f'<h{level} id="{sid}">{inner}</h{level}>'
    return re.sub(r"<h([1-6])>(.*?)</h\1>", sub, body)


def citations(body: str, bib: dict | None, order: list) -> str:
    def sub(m):
        keys = [k.strip() for k in m.group(1).split(",")]
        nums, tips = [], []
        for key in keys:
            if key not in order:
                order.append(key)
            ent = bib.get(key) if bib else None
            nums.append(str(order.index(key) + 1) if ent else "?")
            tips.append(re.sub(r"<[^>]+>", " ", dp.hover_cite(ent)) if ent else "?")
        tip = html.unescape(" | ".join(re.sub(r"\s+", " ", t).strip() for t in tips))
        first = keys[0]
        return (f'<a class="citation cite-group" href="#ref-{html.escape(first)}" '
                f'title="{html.escape(tip)}">[{", ".join(nums)}]</a>')
    return re.sub(r'<d-cite key="([^"]+)"></d-cite>', sub, body)


def footnotes(body: str, notes: list) -> str:
    def sub(m):
        notes.append(m.group(1))
        n = len(notes)
        return (f'<sup class="fn"><a href="#fn-{n}" id="fnref-{n}" '
                f'title="{html.escape(re.sub("<[^>]+>", "", m.group(1)))}">{n}</a></sup>')
    return re.sub(r"<d-footnote>(.*?)</d-footnote>", sub, body, flags=re.S)


def cite_box(fm: dict) -> tuple[str, str]:
    """The kit's 'cite this work' box (distill.html:23-55), for one Anonymous author."""
    title = fm.get("title", "")
    date = fm.get("date")
    when = f"{date:%B} {date.day}, {date.year}" if isinstance(date, (dt.date, dt.datetime)) else ""
    short = ("Anonymous" + "2026" + "".join(title.split(" ")[:3])).replace(" ", "", 1)
    short = "".join(c for c in short if not unicodedata.category(c).startswith("P")
                    and c not in "$+<=>^`|~").lower().strip()
    bibtex = (f"@inproceedings{{{short},\n  author = {{Anonymous, }},\n  title = {{{title}}},\n"
              f"  booktitle = {{TMLR Beyond PDF}},\n  year = {{{when}}}\n}}")
    return f'Anonymous, "{title}", TMLR Beyond PDF, 2026.', bibtex


def submitted_text(fm: dict) -> str:
    sd = fm.get("submitted_date")
    if isinstance(sd, (dt.date, dt.datetime)):
        return f"{DISTILL_MONTHS[sd.month - 1]} {sd.day}, {sd.year}"
    return "Not submitted yet."


def page(fm, sections, toc, refs_html, notes_html, findings_html, counts) -> str:
    css = (SRC / "kit_preview.css").read_text(encoding="utf-8")
    css += styles_line() + "\n" + (SRC / "preview_extra.css").read_text(encoding="utf-8")
    css += HtmlFormatter(style="friendly").get_style_defs(".highlight")
    nav = "".join(f'<div><a href="#{sid}">{html.escape(name)}</a></div>' for name, sid in toc)
    body = []
    for s in sections:
        body.append(s.html)
        label = s.name if s.path.parent.name != "alt" else f"{s.name} (alternate {s.path.name})"
        body.append('<details class="kit-src"><summary>Kit source of this part '
                    f"<code>sections/{html.escape(label)}</code></summary><pre>"
                    f"{html.escape(s.raw)}</pre></details>")
    attribution, bibtex = cite_box(fm)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CHE Paper v2 Preview</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Roboto+Mono:wght@400;500&display=swap">
<style>
{css}
</style></head><body>
<div class="post distill">
<d-title><h1>{html.escape(str(fm.get("title", "")))}</h1><p>{html.escape(str(fm.get("description", "")))}</p></d-title>
<d-byline><div class="byline grid"><div class="authors-affiliations grid">
<h3>Authors</h3><h3>Affiliations</h3>
<p class="author"><span class="name">Anonymous</span></p>
<p class="affiliation"><span class="affiliation">Anonymous</span></p></div>
<div><h3>Submitted</h3><p><em>{html.escape(submitted_text(fm))}</em></p></div>
<div><h3>Status</h3><p class="status-draft"><em>PAPER V2 DRAFT: builder-drafted, not owner-approved. Preview, not the kit build.</em></p></div>
<div><h3>View</h3>
<p class="view-toggle"><label for="show-notes"><input type="checkbox" id="show-notes"> Ledger IDs ({counts["ledger"]}) and comments</label></p>
<p class="view-toggle"><label for="show-print"><input type="checkbox" id="show-print"> Print companions</label></p>
<p class="view-toggle"><label for="show-findings"><input type="checkbox" id="show-findings" checked> Build findings</label></p></div>
</div></d-byline>
<d-article>
<d-contents><nav class="l-text figcaption"><h3>Contents</h3>
{nav}</nav></d-contents>
{findings_html}
{"".join(body)}
<h3 id="footnotes">Footnotes</h3>
{notes_html}
<h3 id="references">References</h3>
<p class="emul-note">Emulated: rendered by a Python port of the kit's Distill code
(normalizeTag, author_string, venue_string, bibliography_cite; checked against the kit's own
JavaScript on all 41 entries). Its field parser re-implements bibtexParse's rules rather than
running it. The real-kit build (<code>kit_build.sh</code>) is authoritative.</p>
{refs_html}
</d-article>
<d-article id="bibtex-container">For attribution in academic contexts, please cite this work as
<pre>{html.escape(attribution)}</pre>BibTeX citation (as the kit's layout builds it; the year field is the kit's)
<pre>{html.escape(bibtex)}</pre></d-article>
</div>
<script>
(function () {{
  function bind(id, cls, invert) {{
    var box = document.getElementById(id);
    var apply = function () {{ document.body.classList.toggle(cls, invert ? !box.checked : box.checked); }};
    box.addEventListener("change", apply); apply();
  }}
  bind("show-notes", "show-notes", false);
  bind("show-print", "show-print", false);
  bind("show-findings", "hide-findings", true);
}})();
window.MathJax = {{
  tex: {{ inlineMath: [["\\\\(", "\\\\)"]], displayMath: [["\\\\[", "\\\\]"]], tags: "ams" }},
  svg: {{ fontCache: "global" }},
  options: {{ skipHtmlTags: ["script", "noscript", "style", "textarea", "pre", "code"] }}
}};
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-svg.js"></script>
</body></html>
"""


def findings_box(rep: Report, m1_flags: list, stub_count: int, unresolved_refs: list) -> str:
    items = []
    for f in rep.failures:
        items.append(f"<li><strong>FAIL</strong> {html.escape(f)}</li>")
    for f in m1_flags:
        items.append(f"<li><strong>M1</strong> sections/{html.escape(f['section'])}:{f['line']} "
                     f"[{html.escape(f['kind'])}] {html.escape(f['why'])}</li>")
    for r in unresolved_refs:
        items.append(f"<li><strong>cross-ref</strong> {html.escape(r['from'])}: "
                     f"{html.escape(r['kind'])} {html.escape(r['label'])} resolves to nothing</li>")
    for w in rep.warnings:
        items.append(f"<li>warning: {html.escape(w)}</li>")
    head = f"Build findings: {stub_count} STUB-SPEC block(s) remain"
    if not items:
        return f'<div class="findings"><h4>{head}; nothing else found.</h4></div>'
    return f'<div class="findings"><h4>{head}</h4><ul>{"".join(items)}</ul></div>'


# ------------------------------------------------------------------- main


def main() -> None:
    ap = argparse.ArgumentParser(description="Build the Paper v2 kit source and preview.")
    ap.add_argument("--root", type=Path, default=V2,
                    help="folder with front_matter.yaml, sections/, ledger files, out/")
    ap.add_argument("--bib", type=Path, default=None,
                    help="bibliography (default <root>/assets/bibliography/submission.bib, "
                         "falling back to paper/v2's)")
    ap.add_argument("--alt", action="append", default=[],
                    help="swap in sections/alt/: a variant name, or NN_slug.variant")
    ap.add_argument("--final", action="store_true",
                    help="also fail on M1 flags, STUB-SPEC blocks, unresolved cross-references, "
                         "placeholders and warnings")
    ap.add_argument("--copy-assets", action="store_true",
                    help="copy the assets into out/ so the preview works from disk")
    ap.add_argument("--styles", type=Path, default=None,
                    help="CSS for the kit's _styles field (default src/kit_styles.css); for "
                         "layout experiments only")
    args = ap.parse_args()
    global STYLES_FILE
    if args.styles:
        STYLES_FILE = args.styles.resolve()
    root = args.root.resolve()
    bib_path = args.bib or root / "assets" / "bibliography" / "submission.bib"
    if not bib_path.exists():
        bib_path = V2 / "assets" / "bibliography" / "submission.bib"
    out = root / "out"
    rep = Report()

    fm = read_front_matter(root, rep)
    ledger, ledger_sources = read_ledgers(root)
    bib_error = None
    try:
        bib = dp.parse_bib(bib_path.read_text(encoding="utf-8"))
    except dp.BibParseError as e:
        bib, bib_error = None, str(e)
        rep.fail(rel(bib_path), f"the kit's BibTeX parser would throw ({e}); "
                 "every citation would lose its entry")
    sections = load_sections(root, args.alt, rep)
    if not sections:
        rep.fail("sections", "no section files")

    seen = {"ids": {}, "cites": []}
    assets: set = set()
    listings, notes_src, m1_flags = [], [], []
    tables = {"md": 0, "html": 0}
    liquid = {"include": 0, "relative_url": 0}
    stub_count, math_n = 0, 0
    for s in sections:
        stub_count += len(re.findall(r"<!--\s*STUB-SPEC\b", s.raw))
        check_tags_and_cites(s, rep, ledger, bib, seen)
        listings += check_listings(s, rep)
        for k, v in check_liquid(s, rep, assets).items():
            liquid[k] += v
        r = m1_scan(s, rep)
        m1_flags += r["flags"]
        tables["md"] += r["md_tables"]
        tables["html"] += r["html_tables"]
        check_footnotes_and_html(s, rep, notes_src)
        math_n += math_count(s.raw)
    if bib is not None:
        raw_bib = dp.parse_bib(bib_path.read_text(encoding="utf-8"), normalize=False)
        for key in sorted(set(seen["cites"]) & set(raw_bib)):
            for name, shown, meant in dp.render_problems(raw_bib[key]):
                rep.warn(rel(bib_path), f"M2: {key}.{name} would show {shown[:70]!r}; "
                         f"it should read {meant[:70]!r}")
            for name, taken in dp.surname_risks(raw_bib[key]):
                rep.warn(rel(bib_path), f"M2: {key}: Distill takes {taken!r} as the surname of "
                         f"{name!r}; write the name 'Last, First' (review RM-5)")
    for rid, row in ledger.items():
        if rid in seen["ids"] and row.get("conflicts"):
            rep.warn("ledger", f"{rid} is defined with different values at {row['source']} "
                     f"and {', '.join(row['conflicts'])}")
    if stub_count:
        rep.final("sections", f"{stub_count} STUB-SPEC block(s) remain")

    # toc from the H2s, checked as the kit links it: '#' + slugify(name) must be the id
    # kramdown gives the heading.
    toc, ids_seen = [], {}
    for s in sections:
        kinds, masked = classify_lines(s.raw)
        for i, ln in enumerate(masked):
            if kinds[i] == "fence":
                continue
            m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", ln)
            if not m:
                continue
            name, kid = m.group(2), dp.kramdown_id(m.group(2))
            ids_seen[kid] = ids_seen.get(kid, -1) + 1
            if len(m.group(1)) != 2:
                continue
            where = f"{s.name}:{i + 1}"
            if ids_seen[kid]:
                rep.fail(where, f"H2 {name!r} repeats an earlier heading id ({kid})")
            if dp.jekyll_slugify(name) != kid:
                rep.fail(where, f"toc name {name!r}: Jekyll slug {dp.jekyll_slugify(name)!r} "
                         f"is not kramdown's id {kid!r}, so the contents link would break")
            if re.search(r'["$`*\\]', name):
                rep.fail(where, f"H2 {name!r} contains a character the toc cannot carry")
            if re.search(r"[.()]", re.sub(r"^\d+\s", "", name)):
                rep.warn(where, f"H2 {name!r} has a dot or parenthesis (INTERFACE: keep them out)")
            toc.append((name, kid))

    targets = collect_targets(sections)
    refs = collect_refs(sections, targets, rep)
    files = resolve_assets(assets, rep, root)

    # ---- outputs
    out.mkdir(parents=True, exist_ok=True)
    header = ["---", "layout: distill",
              f"title: {yaml_scalar(str(fm.get('title', '')))}",
              f"description: {yaml_scalar(str(fm.get('description', '')))}"]
    if fm.get("date") is not None:
        header.append(f"date: {kit_date(fm['date'])}")
    if fm.get("submitted_date") is not None:
        header.append(f"submitted_date: {kit_date(fm['submitted_date'])}")
    header += ["htmlwidgets: true", "authors:"]
    for a in fm.get("authors") or []:
        header += [f"  - name: {a.get('name')}", "    affiliations:",
                   f"      name: {(a.get('affiliations') or {}).get('name')}"]
    header.append("bibliography: submission.bib")
    header.append("toc:")
    header += [f"  - name: {json.dumps(name, ensure_ascii=False)}" for name, _ in toc]
    header += ["_styles: >-", f"  {styles_line()}", "---"]
    kit_src = "\n".join(header) + "\n\n" + "\n\n".join(s.raw.strip() for s in sections) + "\n"
    try:
        parsed = yaml.safe_load(kit_src.split("\n---\n", 1)[0][4:])
        for key in ("title", "description"):
            if parsed.get(key) != fm.get(key):
                rep.fail("header", f"{key} does not survive the YAML round trip")
    except yaml.YAMLError as e:
        rep.fail("header", f"generated YAML header does not parse: {e}")
    (out / "submission_v2.md").write_text(kit_src, encoding="utf-8")

    order: list = []
    fns: list = []
    counter: dict = {}
    for s in sections:
        h = render_section(s.raw, ledger, s.m1_lines)
        h = add_heading_ids(h, counter)
        h = citations(h, bib, order)
        s.html = footnotes(h, fns)
    if bib is None:
        refs_html = (f'<div class="findings"><h4>The kit would show no reference list</h4>'
                     f"<p>bibtexParse would throw: {html.escape(bib_error or '')}</p></div>")
    else:
        refs_html = '<ol class="refs">' + "".join(
            f'<li id="ref-{html.escape(k)}">{dp.bibliography_cite(bib.get(k)) if k in bib else "?"}</li>'
            for k in order) + "</ol>"
    notes_html = ('<ol class="footnotes">' + "".join(
        f'<li id="fn-{n}">{t} <a href="#fnref-{n}">[↩]</a></li>' for n, t in enumerate(fns, 1))
        + "</ol>") if fns else "<p><em>No footnotes.</em></p>"
    unresolved = [r for r in refs if r["target"] is None]
    external = [r for r in refs if r["target"] == "external"]
    findings_html = findings_box(rep, m1_flags, stub_count, unresolved)
    counts = {"ledger": len(seen["ids"])}
    (out / "index.html").write_text(
        page(fm, sections, toc, refs_html, notes_html, findings_html, counts), encoding="utf-8")
    (out / "files.json").write_text(json.dumps(files, indent=1) + "\n", encoding="utf-8")
    if args.copy_assets:
        for pub, src in files.items():
            dst = out / pub
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / src, dst)

    lines = ["# Cross-references (generated by build_v2.py; for the mechanics review)", "",
             f"{len(refs)} references: {len(unresolved)} unresolved, {len(external)} to a cited "
             "work's own numbering (not checked). Targets are the first heading or caption that "
             "defines the label.", "",
             "| from | reference | resolves to | target text |", "|---|---|---|---|"]
    for r in refs:
        tt = (r["target_text"] or "").replace("|", "\\|")
        lines.append(f"| `{r['from']}` | {r['kind']} {r['label']} | "
                     f"{('`' + r['target'] + '`') if r['target'] not in (None, 'external') else ('external' if r['target'] else '**UNRESOLVED**')} | {tt} |")
    (out / "crossrefs.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    fail_final = args.final and (rep.final_failures or rep.warnings)
    report = {
        "root": rel(root), "bib": rel(bib_path), "bib_entries": len(bib or {}),
        "front_matter": {k: (kit_date(v) if isinstance(v, (dt.date, dt.datetime)) else v)
                         for k, v in fm.items()},
        "byline_submitted": submitted_text(fm),
        "cite_box": cite_box(fm)[1],
        "sections": [{"name": s.name, "file": rel(s.path)} for s in sections],
        "alt_available": rep.data.get("alt_available", []), "alt_used": rep.data.get("alt_used", {}),
        "stub_spec_blocks": stub_count,
        "ledger_sources": [rel(p) for p in ledger_sources],
        "ledger_ids_distinct": len(seen["ids"]),
        "ledger_tags": sum(len(v) for v in seen["ids"].values()),
        "cite_tags_keys": len(seen["cites"]), "cite_keys_distinct": len(set(seen["cites"])),
        "cited_keys_in_order": order,
        "listings": listings,
        "m1_flags": m1_flags,
        "tables_source": {"markdown": tables["md"], "html": tables["html"],
                          "total": tables["md"] + tables["html"]},
        "math_source": math_n,
        "liquid": liquid,
        "footnotes": notes_src,
        "toc": [{"name": n, "id": i} for n, i in toc],
        "crossrefs": refs, "crossrefs_unresolved": len(unresolved),
        "assets": len(files),
        "failures": rep.failures, "warnings": rep.warnings,
        "final_only_failures": rep.final_failures,
        "mode": "final" if args.final else "draft",
    }
    (out / "build_report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n",
                                           encoding="utf-8")

    print(f"sections {len(sections)} · toc {len(toc)} · STUB-SPEC {stub_count} · "
          f"ledger IDs {len(seen['ids'])} ({report['ledger_tags']} tags) · "
          f"cites {len(seen['cites'])} ({len(set(seen['cites']))} keys) · "
          f"listings {sum(1 for x in listings if x['ok'])}/{len(listings)} identical · "
          f"tables {report['tables_source']['total']} · math {math_n} · assets {len(files)}")
    print(f"M1 flags {len(m1_flags)}" + "".join(
        f"\n  M1 sections/{f['section']}:{f['line']} [{f['kind']}] {f['text'][:100]}" for f in m1_flags))
    print(f"cross-references {len(refs)} ({len(unresolved)} unresolved; list in out/crossrefs.md)")
    for w in rep.warnings:
        print(f"WARN {w}")
    if args.final:
        for f in rep.final_failures:
            print(f"FAIL(final) {f}")
    for f in rep.failures:
        print(f"FAIL {f}")
    status = "FAIL" if rep.failures or fail_final else "OK"
    print(f"build {status} ({len(rep.failures)} failures, {len(rep.warnings)} warnings"
          f"{', ' + str(len(rep.final_failures)) + ' final-only' if rep.final_failures else ''}) "
          f"-> {rel(out)}/")
    sys.exit(1 if status == "FAIL" else 0)


if __name__ == "__main__":
    main()
