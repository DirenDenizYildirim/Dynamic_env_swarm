"""Check (or write) the v2 bibliography against its only allowed source (M2).

``paper/v2/assets/bibliography/submission.bib`` must be a verbatim copy of the
BibTeX entries in the ```` ```bibtex ```` blocks of
``paper/related_work_verification.md``, in that document's order. This script
splits both files into entries and compares every entry byte for byte.

    python paper/v2/src/bib_diff.py            # check; exit 1 on any difference
    python paper/v2/src/bib_diff.py --write    # regenerate the v2 bib, then check
    python paper/v2/src/bib_diff.py --bib X    # check another file (negative controls)

It also lints every entry for what the kit's Distill renderer cannot show
(``paper/v2/review_of_demo.md`` M2): TeX macros, ``--``, ``$``, inner braces
in a field value, and a bare value that bibtexParse 0.0.22 rejects (anything
but a number or ``jan`` … ``dec``, which makes the whole bibliography fail).
Only ``%`` lines are allowed outside entries, and they may not contain ``@``.
Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "paper" / "related_work_verification.md"
V2_BIB = ROOT / "paper" / "v2" / "assets" / "bibliography" / "submission.bib"
HEADER = (
    "% submission.bib, Paper v2: parsed in the reader's browser by the kit's Distill template.\n"
    "% Every entry is a verbatim copy of a BibTeX block of paper/related_work_verification.md,\n"
    "% in document order, checked by paper/v2/src/bib_diff.py. Never write an entry from memory.\n"
    "% Percent lines are the only additions, never contain an at sign, and are stripped at staging.\n"
)
MONTHS = {"jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"}


def split_entries(text: str) -> list[tuple[str, str]]:
    """Return (key, verbatim entry text) for every ``@type{key, ...}`` in text."""
    out, i = [], 0
    while True:
        m = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,").search(text, i)
        if not m:
            return out
        depth, j = 0, m.start() + len(m.group(0).split("{", 1)[0])
        while j < len(text):
            depth += {"{": 1, "}": -1}.get(text[j], 0)
            j += 1
            if depth == 0:
                break
        else:
            sys.exit(f"unterminated entry {m.group(2)}")
        out.append((m.group(2), text[m.start() : j]))
        i = j


def source_entries() -> list[tuple[str, str]]:
    text = SOURCE.read_text(encoding="utf-8")
    entries = []
    for block in re.findall(r"(?ms)^```bibtex\n(.*?)^```", text):
        entries += split_entries(block)
    return entries


def bib_fields(entry: str) -> list[tuple[str, str, bool]]:
    """(field, value, braced) for each field; values in braces or quotes, or bare."""
    body = entry[entry.index(",") + 1 : entry.rindex("}")]
    fields, i = [], 0
    while True:
        m = re.compile(r"\s*,?\s*([A-Za-z_-]+)\s*=\s*").match(body, i)
        if not m:
            return fields
        j = m.end()
        if body[j] == "{":
            depth, k = 0, j
            while True:
                depth += {"{": 1, "}": -1}.get(body[k], 0)
                k += 1
                if depth == 0:
                    break
            fields.append((m.group(1).lower(), body[j + 1 : k - 1], True))
        elif body[j] == '"':
            k = body.index('"', j + 1) + 1
            fields.append((m.group(1).lower(), body[j + 1 : k - 1], True))
        else:
            b = re.compile(r"[^,}\s]+").match(body, j)
            k = b.end()
            fields.append((m.group(1).lower(), b.group(0), False))
        i = k


def lint(key: str, entry: str) -> list[str]:
    problems = []
    for name, value, braced in bib_fields(entry):
        if not braced and not (value.isdigit() or value.lower() in MONTHS):
            problems.append(f"{key}.{name}: bare value {value!r} makes bibtexParse throw")
        for pat, what in ((r"\\", "TeX macro"), (r"--", "'--'"), (r"\$", "'$'"),
                          (r"[{}]", "inner brace")):
            if re.search(pat, value):
                problems.append(f"{key}.{name}: {what} in {value!r}")
    return problems


def check(src: list[tuple[str, str]], bib_path: Path) -> int:
    text = bib_path.read_text(encoding="utf-8")
    bib = split_entries(text)
    outside = text
    for _, e in bib:
        outside = outside.replace(e, "", 1)
    stray = [ln for ln in outside.splitlines() if ln.strip() and not ln.lstrip().startswith("%")]
    at_in_comment = [ln for ln in outside.splitlines() if ln.lstrip().startswith("%") and "@" in ln]
    src_map = dict(src)
    fails = 0
    print(f"source blocks: {len(src)} entries; v2 bib: {len(bib)} entries")
    if len(set(k for k, _ in src)) != len(src):
        print("FAIL duplicate keys in the source"); fails += 1
    for n, (key, entry) in enumerate(bib):
        if key not in src_map:
            print(f"FAIL {key}: not in any BibTeX block of the source"); fails += 1
        elif entry != src_map[key]:
            print(f"FAIL {key}: differs from its source block"); fails += 1
        elif n >= len(src) or src[n][0] != key:
            print(f"FAIL {key}: out of document order (position {n + 1})"); fails += 1
    for key in sorted(set(src_map) - {k for k, _ in bib}):
        print(f"FAIL {key}: in the source, missing from the v2 bib"); fails += 1
    for ln in stray:
        print(f"FAIL text outside entries that is not a % line: {ln[:80]!r}"); fails += 1
    for ln in at_in_comment:
        print(f"FAIL % line contains '@': {ln[:80]!r}"); fails += 1
    lints = [p for k, e in bib for p in lint(k, e)]
    for p in lints:
        print(f"FAIL lint {p}")
    fails += len(lints)
    same = sum(1 for k, e in bib if src_map.get(k) == e)
    print(f"{same} of {len(bib)} entries byte-identical to their source block; "
          f"{len(lints)} lint findings")
    print("PASS" if fails == 0 else f"FAIL ({fails})")
    return 1 if fails else 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--write", action="store_true", help="regenerate the v2 bib first")
    ap.add_argument("--bib", type=Path, default=V2_BIB,
                    help="check this file instead (negative controls); never written")
    args = ap.parse_args()
    src = source_entries()
    if args.write:
        V2_BIB.parent.mkdir(parents=True, exist_ok=True)
        V2_BIB.write_text(HEADER + "\n" + "\n\n".join(e for _, e in src) + "\n",
                          encoding="utf-8")
        print(f"wrote {V2_BIB.relative_to(ROOT)} ({len(src)} entries)")
    sys.exit(check(src, args.bib))


if __name__ == "__main__":
    main()
