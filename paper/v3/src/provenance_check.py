"""Check each section's per-sentence provenance table against the section's prose.

For every ``<root>/sections/NN_slug.md`` (and each ``sections/alt/*.md``) this splits the
prose into sentences and compares them with the rows of ``<root>/provenance/<same name>``
(format: ``provenance/TEMPLATE.md``). It reports:

- every sentence that has no row (a new or edited sentence nobody sourced);
- every row whose sentence is no longer in the section (stale after an edit);
- rows with an empty support cell, and support it cannot resolve (a ledger ID in no ledger
  source, a cite key not in the v3 bib, a file:line that does not exist).

What counts as a sentence. Comments, fenced code, Liquid tags and lines that hold only
display math are ignored. Headings count. Every list item, figure caption,
``alt``/``caption`` attribute, iframe ``title`` and ``<d-footnote>`` text is split into
sentences on its own. A table row is one unit, written as its cells joined by " / "; it is
also covered if every non-empty cell of the row has its own provenance row. Only tables whose
header's second column starts with "sentence" are read from a provenance file. HTML tags and Markdown emphasis are dropped and
``<d-cite>`` tags removed; inline math is kept as written. Both sides are normalized the
same way before they are compared, so a row may quote the sentence as source or as plain
text.

    python paper/v3/src/provenance_check.py [--root DIR] [NN_slug ...] [--quiet]

Exit 1 if any sentence lacks a row or any row is stale (with ``--strict``, also on a support
problem). Writes ``<root>/out/provenance_check.md`` (or ``--out``). A support path may be repository-relative
or a unique file name in the repository (``git ls-files``).
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # keep src/ free of __pycache__
sys.path.insert(0, str(Path(__file__).resolve().parent))
import distill_port as dp  # noqa: E402

# build_v3.V2 is paper/v3 (the name kept from the v2 tools)
from build_v3 import ID_RE, ROOT, V2, fence_spans, read_ledgers  # noqa: E402

ABBREV = ["e.g.", "i.e.", "et al.", "Fig.", "Figs.", "Eq.", "Eqs.", "App.", "Def.", "Prop.",
          "Thm.", "Cor.", "Sec.", "Sect.", "vs.", "cf.", "approx.", "Tab.",
          "resp.", "ca.", "Dr.", "St.", "Jr.", "etc.)", "Ref.", "Refs.", "Alg."]
# Abbreviations that are abbreviations only before a number ("p. 12", "pp. 3–4", "No. 5"):
# "p." ending "step." or "group." is a sentence end.
ABBREV_BEFORE_NUMBER = ["pp.", "p.", "No."]


def normalize(s: str) -> str:
    s = html.unescape(s)
    s = s.replace("\\|", "|")
    s = re.sub(r"<d-cite\b[^>]*>\s*</d-cite>", "", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\*\*|__|`", "", s)
    s = re.sub(r"(?<![\w$\\])\*(?=\S)|(?<=\S)\*(?![\w$])", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([,.;:!?)])", r"\1", s)
    return s


def split_sentences(text: str) -> list[str]:
    text = normalize(text)
    if not text:
        return []
    store = []

    def keep(m):
        store.append(m.group(0))
        return f"\x00{len(store) - 1}\x00"

    text = re.sub(r"\$[^$]+\$", keep, text)                      # never split inside math
    for a in ABBREV:   # whole words only: "Prop." but not the end of "Isoprop."
        text = re.sub(r"(?<![\w.])" + re.escape(a), a.replace(".", "\x01"), text)
    for a in ABBREV_BEFORE_NUMBER:
        text = re.sub(r"(?<![\w.])" + re.escape(a) + r"(?=\s?\d)", a.replace(".", "\x01"), text)
    text = re.sub(r"\b([A-Z])\.(?=\s?[A-Z])", "\\1\x01", text)   # initials: J. Smith
    parts = re.split(r"(?<=[.!?])[\"”’)]?\s+(?=[\"“(§\[]?[A-Z0-9ΓΔΘΛΞΠΣΦΨΩαβγδεκλμνξπρστφχψω\x00])", text)
    out = []
    carry = ""
    for p in parts:
        p = p.replace("\x01", ".")
        p = re.sub(r"\x00(\d+)\x00", lambda m: store[int(m.group(1))], p).strip()
        # a run-in label ("Figure 5.", "Remark 1 (Hardness).") belongs to what follows it
        if re.fullmatch(r"[A-Z][a-z]+\.? [A-Z]?\d+[′″']*(?: \([^)]*\))?\.", p):
            carry = (carry + " " + p).strip()
            continue
        p = (carry + " " + p).strip()
        carry = ""
        if re.search(r"[A-Za-z0-9]", p):
            out.append(p)
    if carry:
        out.append(carry)
    return out


CELLS: dict[str, list[str]] = {}   # table-row unit -> its cells (a row may be sourced per cell)


def section_units(raw: str) -> list[tuple[int, str]]:
    """(line, sentence) in document order."""
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), raw, flags=re.S)
    lines = text.split("\n")
    for a, b, _ in fence_spans(lines):
        for k in range(a, b + 1):
            lines[k] = ""
    units: list[tuple[int, str]] = []
    para, start = [], 0

    def flush():
        nonlocal para
        if para:
            for s in split_sentences(" ".join(para)):
                units.append((start, s))
        para = []

    in_display = False
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if s == "$$" or (s.startswith("$$") and s.endswith("$$") and len(s) > 4 and not in_display):
            if s == "$$":
                in_display = not in_display
            flush()
            continue
        if in_display:
            continue
        carriers = []
        for m in re.finditer(r'\b(?:alt|caption|title)="([^"]*)"', s):
            carriers.append(m.group(1))
        for m in re.finditer(r"<d-footnote>(.*?)</d-footnote>", s):
            carriers.append(m.group(1))
        s = re.sub(r"<d-footnote>.*?</d-footnote>", "", s)
        s = re.sub(r"\{%.*?%\}|\{\{.*?\}\}", "", s)
        s = re.sub(r"<(?:iframe|img)\b[^>]*>", "", s)
        for c in carriers:
            for sent in split_sentences(c):
                units.append((i, sent))
        if re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{1,}:?\s*)*\|?\s*$", s) and "-" in s:
            continue
        if not s:
            flush()
            continue
        if s.startswith("|"):
            flush()
            cells = [normalize(c) for c in re.split(r"(?<!\\)\|", s.strip().strip("|"))]
            cells = [c for c in cells if re.search(r"[A-Za-z0-9]", c)]
            if cells:
                CELLS[normalize(" / ".join(cells))] = cells
                units.append((i, normalize(" / ".join(cells))))
            continue
        if re.match(r"^#{1,6}\s", s):
            flush()
            units.append((i, normalize(re.sub(r"^#{1,6}\s+", "", s))))
            continue
        m = re.match(r"^(?:[-*+]|\d+\.)\s+(.*)$", s)
        if m:
            flush()
            start, para = i, [m.group(1)]
            continue
        s = re.sub(r"^(>\s*)+", "", s)
        if not para:
            start = i
        para.append(s)
    flush()
    return [(n, u) for n, u in units if u]


def provenance_rows(path: Path) -> list[dict]:
    """Rows of every table whose header's second column starts with 'sentence'; other
    tables (title candidates, findings) are ignored."""
    rows, in_table, prev_blank = [], False, True
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        s = line.strip()
        if not s.startswith("|"):
            in_table = False
            continue
        body = s[1:-1] if s.endswith("|") and not s.endswith("\\|") else s[1:]
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", body)]
        if re.fullmatch(r"[\s|:-]+", s):
            continue
        if len(cells) >= 2 and cells[1].lower().startswith("sentence"):
            in_table = True
            continue
        if not in_table or len(cells) < 3:
            continue
        rows.append({"line": n, "num": cells[0], "sentence": cells[1], "support": cells[2],
                     "change": cells[3] if len(cells) > 3 else ""})
    return rows


_TRACKED: list[str] = []


def tracked_files() -> list[str]:
    """Repository files (git ls-files, read-only), to resolve a support path given short."""
    if not _TRACKED:
        import subprocess
        _TRACKED.extend(subprocess.run(["git", "-C", str(ROOT), "ls-files"], capture_output=True,
                                       text=True).stdout.splitlines())
    return _TRACKED


def check_support(sup: str, ledger: dict, bib: dict) -> list[str]:
    problems = []
    if not sup.strip():
        return ["empty support"]
    low = sup.lower()
    recognized = False
    if "framing" in low:
        recognized = True
    for rid in re.findall(rf"\b{ID_RE}\b", sup):
        if re.fullmatch(r"[A-Z]+\d*-?\d+[a-z]?", rid) and "-" in rid:
            recognized = True
            if rid not in ledger:
                problems.append(f"ledger ID {rid} resolves in no ledger source")
            elif ledger[rid].get("pending"):
                problems.append(f"ledger ID {rid} is a PENDING row ({ledger[rid]['source']})")
    for m in re.finditer(r"`?([\w./-]+\.\w+):(\d+)(?:[-–](\d+))?`?", sup):
        recognized = True
        p = ROOT / m.group(1)
        if not p.exists():
            hits = [f for f in tracked_files() if f.endswith("/" + m.group(1).lstrip("./"))]
            if len(hits) != 1:
                problems.append(f"{m.group(1)}: {'no' if not hits else len(hits)} matching file"
                                f"{'s' if len(hits) > 1 else ''} in the repository")
                continue
            p = ROOT / hits[0]
        n = len(p.read_text(encoding="utf-8", errors="replace").splitlines())
        if int(m.group(3) or m.group(2)) > n:
            problems.append(f"{m.group(0)} is past the end of the file ({n} lines)")
    for key in re.findall(r"\b([a-z]+\d{4}[a-z]+)\b", sup):
        recognized = True
        if key not in bib:
            problems.append(f"cite key {key} is not in the v3 bib")
    if "decision log" in low or "decision_log" in low or re.search(r"\b[A-Z][A-Z ]{3,}\b", sup):
        recognized = True
    if not recognized:
        problems.append("support is not a ledger ID, file:line, cite key, decision-log entry or 'framing'")
    return problems


def main() -> None:
    ap = argparse.ArgumentParser(description="Check provenance tables against sections.")
    ap.add_argument("names", nargs="*", help="section names (NN_slug); default all")
    ap.add_argument("--root", type=Path, default=V2)
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--strict", action="store_true", help="also fail on support problems")
    ap.add_argument("--out", type=Path, default=None, help="where provenance_check.md goes "
                    "(default <root>/out)")
    a = ap.parse_args()
    root = a.root.resolve()
    ledger, _ = read_ledgers(root)
    bib_path = root / "assets" / "bibliography" / "submission.bib"
    if not bib_path.exists():
        bib_path = V2 / "assets" / "bibliography" / "submission.bib"
    bib = dp.parse_bib(bib_path.read_text(encoding="utf-8"))
    files = sorted((root / "sections").glob("*.md")) + sorted((root / "sections" / "alt").glob("*.md"))
    if a.names:
        files = [f for f in files if f.stem in a.names or f.name in a.names]
    report, bad = ["# Provenance check (generated by provenance_check.py)", ""], 0
    for f in files:
        units = section_units(f.read_text(encoding="utf-8"))
        prov = root / "provenance" / f.name
        head = f"## {f.relative_to(root)}"
        if not prov.exists() and not units:
            print(f"{f.name}: no sentences yet, no provenance file needed")
            continue
        if not prov.exists():
            report += [head, "", f"No `provenance/{f.name}`: {len(units)} sentences unsourced.", ""]
            print(f"{f.name}: {len(units)} sentences, NO provenance file")
            bad += 1
            continue
        rows = provenance_rows(prov)
        want = {}
        for n, u in units:
            want.setdefault(u, []).append(n)
        have = {}
        for r in rows:
            have.setdefault(normalize(r["sentence"]), []).append(r)
        cells_of = {u: CELLS[u] for u in want if u in CELLS}
        all_cells = {c for cs in cells_of.values() for c in cs}
        missing = [(n, u) for n, u in units if u not in have
                   and not (u in cells_of and all(c in have for c in cells_of[u]))]
        stale = [r for r in rows if normalize(r["sentence"]) not in want
                 and normalize(r["sentence"]) not in all_cells]
        support = [(r, p) for r in rows for p in check_support(r["support"], ledger, bib)]
        bad += bool(missing or stale or (a.strict and support))
        print(f"{f.name}: {len(units)} sentences, {len(rows)} rows; {len(missing)} without a row, "
              f"{len(stale)} stale rows, {len(support)} support problems")
        report += [head, "", f"{len(units)} sentences, {len(rows)} rows: {len(missing)} without a row, "
                   f"{len(stale)} stale, {len(support)} support problems.", ""]
        if missing:
            report += ["Sentences with no row:", ""] + [f"- `{f.name}:{n}` {u}" for n, u in missing] + [""]
        if stale:
            report += ["Rows whose sentence is no longer in the section:", ""] + \
                      [f"- `provenance/{f.name}:{r['line']}` (row {r['num']}) {r['sentence'][:200]}" for r in stale] + [""]
        if support:
            report += ["Support problems:", ""] + \
                      [f"- `provenance/{f.name}:{r['line']}` (row {r['num']}): {p}" for r, p in support] + [""]
        if not a.quiet:
            for n, u in missing:
                print(f"  NO ROW  {f.name}:{n}  {u[:110]}")
            for r in stale:
                print(f"  STALE   provenance/{f.name}:{r['line']}  {r['sentence'][:110]}")
            for r, p in support:
                print(f"  SUPPORT provenance/{f.name}:{r['line']}  {p}")
    out = (a.out or root / "out").resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / "provenance_check.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"{'FAIL' if bad else 'OK'}: {bad} section(s) with unsourced or stale sentences "
          f"-> {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}/provenance_check.md")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
