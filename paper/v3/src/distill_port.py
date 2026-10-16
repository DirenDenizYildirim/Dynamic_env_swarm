"""Python ports of the kit code that decides what a reader sees (shared by the v2 tools).

Ported line by line from the TMLR Beyond PDF author kit (sha256 ``e531434b…bacc2d5``,
``KIT_NOTES.md`` §S1.1), file ``tmlr_do_not_modify/assets/js/distillpub/template.v2.js``:

- ``normalize_tag``      <- ``normalizeTag`` (:1976-1981)
- ``author_string``      <- ``author_string`` (:915-958)
- ``venue_string``       <- ``venue_string`` (:960-976)
- ``link_string``        <- ``link_string`` (:978-997)
- ``doi_string``         <- ``doi_string`` (:998-1005)
- ``bibliography_cite``  <- ``bibliography_cite`` (:1011-1043)
- ``hover_cite``         <- ``hover_cite`` (:1045-1064)
- ``parse_bib``          <- the value rules of bibtexParse 0.0.22 (:1662-1971): braces and
  quotes keep their inner text verbatim; a bare value must be a number or a month
  abbreviation ``jan`` … ``dec`` (lower-cased), and anything else throws, which in the
  browser makes the whole bibliography fail to load.

The parser is a re-implementation, not bibtexParse itself, so the preview labels its
reference list as an emulation; ``kit_build.sh`` renders the real thing.

Also here: ``kramdown_id`` (kramdown-parser-gfm's ``generate_gfm_header_id``), ``jekyll_slugify``
(Jekyll's ``slugify``, default mode, as the kit's ``toc`` links use it), and ``tex_to_unicode``
(what a TeX field *should* read, used to catch Distill's silent accent drops).
"""

from __future__ import annotations

import re
import unicodedata

MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]


class BibParseError(Exception):
    """bibtexParse would throw here; the kit's bibliography then fails as a whole."""


# ------------------------------------------------------------------ parsing


def _value(s: str, i: int) -> tuple[str, int]:
    if s[i] == "{":
        depth, j = 0, i
        while j < len(s):
            depth += {"{": 1, "}": -1}.get(s[j], 0)
            if depth == 0:
                return s[i + 1 : j], j + 1
            j += 1
        raise BibParseError("unterminated braces")
    if s[i] == '"':
        j = s.index('"', i + 1)
        return s[i + 1 : j], j + 1
    m = re.compile(r"[^,{} =]+").match(s, i)
    if not m:
        raise BibParseError(f"value expected at {s[i:i + 30]!r}")
    word = m.group(0)
    if word.isdigit():
        return word, m.end()
    if word.lower() in MONTHS:
        return word.lower(), m.end()
    raise BibParseError(f"Value expected: {word!r} (bare word, not a number or month)")


RENDERED = ("title", "author", "year", "date", "journal", "booktitle", "volume", "number",
            "issue", "pages", "publisher", "doi", "url")


def parse_bib(text: str, normalize: bool = True) -> dict[str, dict[str, str]]:
    """key -> {field: normalized value, 'type': entry type}; ``%`` lines dropped.
    With ``normalize=False`` the values are returned as written (for comparisons).

    bibtexParse itself skips anything before an ``@``; ``%`` lines are dropped here for
    the same effect (they must never contain ``@``)."""
    text = "\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith("%"))
    out: dict[str, dict[str, str]] = {}
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        fields: dict[str, str] = {}
        i = m.end()
        while True:
            f = re.compile(r"\s*([^,{}\s=]+)\s*=\s*").match(text, i)
            if not f:
                break
            parts = []
            val, i = _value(text, f.end())
            parts.append(val)
            while (h := re.compile(r"\s*#\s*").match(text, i)):
                val, i = _value(text, h.end())
                parts.append(val)
            value = "".join(parts)
            fields[f.group(1).lower()] = normalize_tag(value) if normalize else value
            c = re.compile(r"\s*,?").match(text, i)
            i = c.end()
        fields["type"] = m.group(1)
        out[m.group(2)] = fields
    return out


def normalize_tag(s: str) -> str:
    s = re.sub(r"[\t\n ]+", " ", s)
    s = re.sub(r"\{\\[\"^`.'acu~Hvs]( )?([a-zA-Z])\}", lambda m: m.group(2), s)
    return re.sub(r"\{\\([a-zA-Z])\}", lambda m: m.group(1), s)


# --------------------------------------------------------------- rendering


def author_string(ent: dict, template: str, sep: str, final_sep: str | None = None) -> str:
    if ent.get("author") is None:
        return ""
    names = ent["author"].split(" and ")
    strings = []
    for name in names:
        name = name.strip()
        firsts = None
        if "," in name:
            last = name.split(",")[0].strip()
            firsts = name.split(",")[1]
        elif " " in name:
            last = name.split(" ")[-1].strip()
            firsts = " ".join(name.split(" ")[:-1])
        else:
            last = name.strip()
        initials = ""
        if firsts is not None:
            initials = ".".join(s.strip()[:1] for s in firsts.strip().split(" ")) + "."
        out = template.replace("${F}", firsts if firsts is not None else "undefined", 1)
        strings.append(out.replace("${L}", last, 1).replace("${I}", initials, 1).strip())
    if len(names) > 1:
        return sep.join(strings[:-1]) + (final_sep or sep) + strings[-1]
    return strings[0]


def venue_string(ent: dict) -> str:
    cite = ent.get("journal") or ent.get("booktitle") or ""
    if "volume" in ent:
        issue = ent.get("issue") or ent.get("number")
        issue = f"({issue})" if issue is not None else ""
        cite += ", Vol " + ent["volume"] + issue
    if "pages" in ent:
        cite += ", pp. " + ent["pages"]
    if cite != "":
        cite += ". "
    if "publisher" in ent:
        cite += ent["publisher"]
        if cite[-1] != ".":
            cite += "."
    return cite


def link_string(ent: dict) -> str:
    if "url" not in ent:
        return ""
    url = ent["url"]
    m = re.search(r"arxiv\.org/abs/([0-9.]*)", url)
    if m:
        url = f"http://arxiv.org/pdf/{m.group(1)}.pdf"
    label = "PDF" if url[-4:] == ".pdf" else "HTML" if url[-5:] == ".html" else "link"
    return f' &ensp;<a href="{url}">[{label}]</a>'


def doi_string(ent: dict, new_line: bool = False) -> str:
    if "doi" not in ent:
        return ""
    br = "<br>" if new_line else ""
    return (f'{br} <a href="https://doi.org/{ent["doi"]}" '
            f'style="text-decoration:inherit;">DOI: {ent["doi"]}</a>')


def bibliography_cite(ent: dict | None) -> str:
    if not ent:
        return "?"
    cite = '<span class="title">' + ent.get("title", "undefined") + "</span> "
    cite += link_string(ent) + "<br>"
    year = ent.get("year") or ent.get("date")
    if ent.get("author"):
        cite += author_string(ent, "${L}, ${I}", ", ", " and ")
        if year:
            cite += ", "
    cite += (year + ". ") if year else ". "
    cite += venue_string(ent)
    cite += doi_string(ent)
    return cite


def hover_cite(ent: dict | None) -> str:
    if not ent:
        return "?"
    title = ent.get("title", "undefined")
    cite = "<strong>" + title + "</strong>" + link_string(ent) + "<br>"
    a_str = author_string(ent, "${I} ${L}", ", ") + "."
    v_str = venue_string(ent).strip() + " " + str(ent.get("year", "undefined")) + ". " + doi_string(ent, True)
    if len(a_str + v_str) < min(40, len(title)):
        return cite + a_str + " " + v_str
    return cite + a_str + "<br>" + v_str


# ---------------------------------------------------------------- headings


def kramdown_id(raw: str) -> str:
    """kramdown-parser-gfm ``generate_gfm_header_id`` (no counter suffix)."""
    s = re.sub(r"[^\w\- \t]", "", raw.lower())
    return re.sub(r"[ \t]", "-", s)


def jekyll_slugify(s: str) -> str:
    """Jekyll ``slugify`` default mode: runs of non-alphanumerics -> '-', trimmed, lower."""
    return re.sub(r"[\W_]+", "-", s).strip("-").lower()


# ------------------------------------------------------------- TeX -> text

_ACC = {'"': "\u0308", "'": "\u0301", "^": "\u0302", "~": "\u0303", "`": "\u0300",
        "c": "\u0327", "=": "\u0304", ".": "\u0307", "u": "\u0306", "v": "\u030c",
        "H": "\u030b"}


def render_problems(raw: dict) -> list[tuple[str, str, str]]:
    """(field, what Distill shows, what the field means) for each rendered field of one
    raw entry that shows raw TeX or differs from its intended Unicode (a dropped accent)."""
    out = []
    for name in RENDERED:
        if name not in raw:
            continue
        shown, meant = normalize_tag(raw[name]).strip(), tex_to_unicode(raw[name])
        if shown != meant or re.search(r"[\\{}$]|--", shown):
            out.append((name, shown, meant))
    return out


PARTICLES = {"de", "van", "von", "der", "den", "da", "di", "du", "la", "le", "del", "dos", "das",
             "ter", "ten", "bin", "ibn", "al", "el", "abu", "st", "mac"}


def surname_risks(raw: dict) -> list[tuple[str, str]]:
    """(name, what Distill takes as its surname) for each author written "First ... Last"
    whose surname likely has more than one word (a particle such as "de", "van", "Al"
    before the last word). Distill splits such a name at its last space; "Last, First"
    avoids that (review RM-5)."""
    out = []
    for name in (raw.get("author") or "").split(" and "):
        name = name.strip()
        words = name.split()
        if "," in name or len(words) < 3:
            continue
        if any(w.lower().strip(".") in PARTICLES for w in words[1:-1]):
            out.append((name, words[-1]))
    return out


def tex_to_unicode(v: str) -> str:
    """What a BibTeX field is meant to read, for comparison with what Distill shows.
    Identity on a field that is already plain Unicode."""
    v = re.sub(r"[\t\n ]+", " ", v)
    v = re.sub(r"\$\\frac\{(\d+)\}\{(\d+)\}\$", r"\1/\2", v)
    v = re.sub(r"\{\\([\"'^~`=.uvHc])\s?\{?([A-Za-z])\}?\}",
               lambda m: m.group(2) + _ACC[m.group(1)], v)
    v = re.sub(r"\\([\"'^~`=.])\{?([A-Za-z])\}?", lambda m: m.group(2) + _ACC[m.group(1)], v)
    v = re.sub(r"\\([uvHc])\{([A-Za-z])\}", lambda m: m.group(2) + _ACC[m.group(1)], v)
    for a, b in ((r"{\i}", "\u0131"), (r"\i ", "\u0131"), (r"\dh ", "\u00f0"),
                 (r"\dh{}", "\u00f0"), (r"{\ss}", "\u00df"), (r"{\o}", "\u00f8"),
                 (r"{\O}", "\u00d8"), (r"{\l}", "\u0142"), (r"{\L}", "\u0141"),
                 (r"{\aa}", "\u00e5"), (r"{\AA}", "\u00c5"),
                 (r"\textquotesingle ", "'"), (r"\&", "&"), ("``", "\u201c"),
                 ("''", "\u201d"), ("---", "\u2014"), ("--", "\u2013")):
        v = v.replace(a, b)
    v = v.replace("{", "").replace("}", "")
    return unicodedata.normalize("NFC", v).strip()
