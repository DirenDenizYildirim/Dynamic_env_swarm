"""Build the Beyond PDF demonstration (DEMONSTRATION DRAFT ruling, 2026-10-11).

Reads the owner's front matter and abstract from ``paper/finale.md`` (verbatim)
and the builder-written sections in ``paper/demo_beyond/sections/``, then writes:

- ``paper/demo_beyond/submission_demo.md``: the kit-format source, i.e. what
  ``submission_folder/submission.md`` would hold (YAML header, Markdown,
  Liquid includes, MathJax, ``<d-cite>``), with a generated ``toc``;
- ``paper/demo_beyond/out/index.html``: a static preview of that source in
  the kit's Distill look (CSS copied from the kit, see ``kit_preview.css``),
  with ledger IDs and comments shown on demand and each section's source
  beside it;
- ``paper/demo_beyond/out/files.json``: published path -> repository file, for
  every asset the page references.

The preview imitates the kit; it is not the kit's Jekyll build
(``paper/beyond_pdf/KIT_NOTES.md`` §S4 is still owed). Run from the repo root:
``.venv/bin/python paper/demo_beyond/src/build_demo.py``.
"""

from __future__ import annotations

import html
import json
import re
import sys
import unicodedata
from pathlib import Path

import yaml
from markdown_it import MarkdownIt
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

ROOT = Path(__file__).resolve().parents[3]
DEMO = ROOT / "paper" / "demo_beyond"
SRC = DEMO / "src"
OUT = DEMO / "out"
FINALE = ROOT / "paper" / "finale.md"
BIB = ROOT / "paper" / "beyond_pdf" / "assets" / "bibliography" / "submission.bib"
LEDGERS = [
    ROOT / "paper" / "numbers_ledger.md",
    DEMO / "ledger_supplement.md",
    *sorted((DEMO / "ledger_proposals").glob("*.md")),
]
# Page style the kit inlines from the YAML `_styles` field (KIT_NOTES §S1.4):
# the iframe is the screen figure, its static companion the print figure.
KIT_STYLES = (
    ".print-companion { display: none; } "
    "@media print { .print-companion { display: block; } "
    "d-article figure iframe { display: none; } }"
)
# Where each kit asset directory's files come from (basename lookup).
ASSET_DIRS = {
    "html": ["paper/figures/interactive/out/html", "paper/figures/out/html"],
    "img": [
        "paper/figures/interactive/out/img",
        "paper/figures/out/img",
        "paper/renders/2026-10-10/img",
    ],
    "gif": ["paper/figures/out/gif", "paper/renders/2026-10-10/gif"],
}
HEADER_TAG = "BUILDER-WRITTEN DEMONSTRATION"


# ----------------------------------------------------------------- inputs


def read_finale() -> tuple[dict, str, str]:
    """Return (front matter dict, raw front matter text, abstract markdown)."""
    text = FINALE.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        sys.exit("finale.md: no YAML front matter")
    front_raw, body = m.group(1), m.group(2)
    abstract = body.split("\n## ", 1)[0].strip()
    return yaml.safe_load(front_raw), front_raw, abstract


def read_ledgers() -> dict[str, str]:
    """Map ledger row ID -> 'value — what' for the tooltip of each ID chip."""
    rows: dict[str, str] = {}
    for path in LEDGERS:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 3 and re.fullmatch(r"[A-Z]+-?\d+[a-z]?", cells[0]):
                rows[cells[0]] = f"{cells[1]} — {cells[2]}"
    return rows


def _bib_value(s: str, i: int) -> tuple[str, int]:
    """Read one brace- or quote-delimited BibTeX value starting at s[i]."""
    if s[i] == "{":
        depth, j = 0, i
        while j < len(s):
            depth += {"{": 1, "}": -1}.get(s[j], 0)
            if depth == 0:
                return s[i + 1 : j], j + 1
            j += 1
    if s[i] == '"':
        j = s.index('"', i + 1)
        return s[i + 1 : j], j + 1
    m = re.match(r"[^,\n}]+", s[i:])
    return m.group(0).strip(), i + m.end()


def read_bib() -> dict[str, dict[str, str]]:
    text = "\n".join(
        ln for ln in BIB.read_text(encoding="utf-8").splitlines()
        if not ln.lstrip().startswith("%")
    )
    entries: dict[str, dict[str, str]] = {}
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        fields, i = {"_type": m.group(1).lower()}, m.end()
        while True:
            f = re.compile(r"\s*(\w+)\s*=\s*").match(text, i)
            if not f:
                break
            val, i = _bib_value(text, f.end())
            fields[f.group(1).lower()] = re.sub(r"\s+", " ", val).strip()
            c = re.compile(r"\s*,?").match(text, i)
            i = c.end()
        entries[m.group(2)] = fields
    return entries


def _distill_tex(s: str) -> str:
    """What Distill's bib renderer does to a field (KIT_NOTES §S1.5): collapse
    whitespace and resolve only {\\"a}-style umlauts and {\\i}; every other
    LaTeX form shows as literal text, as it does on the kit's page."""
    s = re.sub(r'\{\\"([A-Za-z])\}', lambda m: unicodedata.normalize(
        "NFC", m.group(1) + "\u0308"), s)
    return re.sub(r"\s+", " ", s.replace("{\\i}", "\u0131")).strip()


def _detex(s: str) -> str:
    s = re.sub(r"\\[a-zA-Z]+\{([^{}]*)\}", r"\1", s)
    return s.replace("{", "").replace("}", "").replace("--", "–").replace("\\&", "&")


def _short_authors(authors: str) -> str:
    names = [a.strip() for a in authors.split(" and ") if a.strip()]
    last = [_detex(n.split(",")[0] if "," in n else n.split()[-1]) for n in names]
    if len(last) == 1:
        return last[0]
    if len(last) == 2:
        return f"{last[0]} & {last[1]}"
    return f"{last[0]} et al."


# ----------------------------------------------------------- transforms


class Section:
    """One section file: raw kit source and its preview HTML."""

    def __init__(self, path: Path, raw: str):
        self.path, self.raw, self.html = path, raw, ""


def _protect(pattern: str, text: str, store: list[str], tag: str, flags=0) -> str:
    def sub(m: re.Match) -> str:
        store.append(m.group(0))
        return f"{tag}{len(store) - 1}Q"

    return re.sub(pattern, sub, text, flags=flags)


def _restore(text: str, store: list[str], tag: str, fn=lambda s: s) -> str:
    return re.sub(rf"{tag}(\d+)Q", lambda m: fn(store[int(m.group(1))]), text)


def comments_to_notes(text: str, ledger: dict[str, str], seen: dict) -> str:
    """Ledger comments become ID chips; other comments become hidden notes."""

    def ledger_chip(m: re.Match) -> str:
        ids = [x.strip() for x in m.group(1).split(",")]
        chips = []
        for rid in ids:
            seen["ledger"].add(rid)
            tip = ledger.get(rid)
            if tip is None:
                seen["missing"].add(rid)
                tip = "NOT IN LEDGER"
            chips.append(
                f'<span class="note note-ledger" title="{html.escape(tip)}">'
                f"{html.escape(rid)}</span>"
            )
        return "".join(chips)

    text = re.sub(r"<!--\s*N:\s*([A-Za-z0-9,\s-]+?)\s*-->", ledger_chip, text)

    def block(m: re.Match) -> str:
        body = m.group(1).strip()
        if body.startswith(HEADER_TAG):
            return ""
        seen["notes"] += 1
        return (
            '\n<div class="note note-block"><span class="note-tag">hidden comment'
            f"</span>{html.escape(body)}</div>\n"
        )

    text = re.sub(r"^[ \t]*<!--(.*?)-->[ \t]*$", block, text, flags=re.S | re.M)

    def inline(m: re.Match) -> str:
        seen["notes"] += 1
        note = html.escape(m.group(1).strip())
        return f'<span class="note note-inline">{note}</span>'

    return re.sub(r"<!--(.*?)-->", inline, text, flags=re.S)


def liquid(text: str, assets: set[str]) -> str:
    """Expand the two Liquid forms the kit uses; refuse any other."""

    def rel(m: re.Match) -> str:
        assets.add(m.group(1))
        return m.group(1)

    text = re.sub(r"\{\{\s*'([^']+)'\s*\|\s*relative_url\s*\}\}", rel, text)

    def include(m: re.Match) -> str:
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        path = attrs.get("path", "")
        assets.add(path)
        cls = attrs.get("class", "img-fluid rounded")
        alt = html.escape(attrs.get("alt", ""), quote=True)
        style = f' style="{attrs["style"]}"' if "style" in attrs else ""
        cap = attrs.get("caption", "")
        cap_html = f'<figcaption class="caption">{cap}</figcaption>' if cap else ""
        return (
            f'\n<figure class="kit-figure"><picture><img src="{path}" class="{cls}"'
            f' alt="{alt}"{style} loading="lazy"></picture>{cap_html}</figure>\n'
        )

    text = re.sub(r"\{%\s*include\s+figure\.html\s+(.*?)%\}", include, text, flags=re.S)
    for bad in ("{{", "{%"):
        if bad in text:
            line = text[: text.index(bad)].count("\n") + 1
            sys.exit(f"unsupported Liquid '{bad}' near line {line}")
    return text


def protect_math(text: str, store: list[str]) -> str:
    """Replace kit math ($$…$$ display or inline, $…$ inline) with tokens."""
    text = text.replace("\\$", "DOLLARQ")

    def disp(m: re.Match) -> str:
        store.append(("display", m.group(1)))
        return f"\n\nMXQ{len(store) - 1}Q\n\n"

    text = re.sub(r"(?m)^[ \t]*\$\$(.+?)\$\$[ \t]*$", disp, text, flags=re.S | re.M)

    def inl(m: re.Match) -> str:
        store.append(("inline", m.group(1) or m.group(2)))
        return f"MXQ{len(store) - 1}Q"

    inline_math = r"\$\$(.+?)\$\$|(?<![\\\w])\$([^\s$](?:[^$\n]*?[^\s$])?)\$"
    return re.sub(inline_math, inl, text)


def restore_math(text: str, store: list) -> str:
    def sub(m: re.Match) -> str:
        kind, tex = store[int(m.group(1))]
        tex = html.escape(tex.strip(), quote=False)
        if kind == "display":
            return f'<div class="math-display">\\[{tex}\\]</div>'
        return f"\\({tex}\\)"

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


def render_markdown(text: str, ledger, seen, assets) -> str:
    code: list[str] = []
    text = _protect(r"(?ms)^```.*?^```[ \t]*$", text, code, "FNQ")
    text = _protect(r"`[^`\n]+`", text, code, "ICQ")
    text = comments_to_notes(text, ledger, seen)
    text = liquid(text, assets)
    math: list = []
    text = protect_math(text, math)
    text = _restore(text, code, "ICQ")
    text = _restore(text, code, "FNQ")
    return restore_math(MD.render(text), math)


def slugify(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", html.unescape(s)).lower()
    return re.sub(r"[^\w]+", "-", s).strip("-")


def add_heading_ids(body: str, toc: list) -> str:
    def sub(m: re.Match) -> str:
        level, inner = m.group(1), m.group(2)
        plain = re.sub(r"<[^>]+>", "", inner)
        sid = slugify(inner)
        toc.append((int(level), html.unescape(plain), sid))
        return f'<h{level} id="{sid}">{inner}</h{level}>'

    return re.sub(r"<h([23])>(.*?)</h\1>", sub, body)


def citations(body: str, bib: dict, order: list[str], missing: set) -> str:
    def sub(m: re.Match) -> str:
        out = []
        for key in [k.strip() for k in m.group(1).split(",")]:
            if key not in bib:
                missing.add(key)
                out.append(f'<span class="cite-missing">[{html.escape(key)}?]</span>')
                continue
            if key not in order:
                order.append(key)
            e = bib[key]
            tip = f"{_short_authors(e.get('author', '?'))} ({e.get('year', '?')}). "
            tip += _detex(e.get("title", ""))
            out.append(
                f'<a class="citation" href="#ref-{key}" '
                f'title="{html.escape(tip)}">{order.index(key) + 1}</a>'
            )
        return '<span class="cite-group">[' + ", ".join(out) + "]</span>"

    return re.sub(r'<d-cite key="([^"]+)"></d-cite>', sub, body)


def footnotes(body: str, notes: list[str]) -> str:
    def sub(m: re.Match) -> str:
        notes.append(m.group(1))
        n = len(notes)
        return (
            f'<sup class="fn"><a href="#fn-{n}" id="fnref-{n}" '
            f'title="{html.escape(re.sub("<[^>]+>", "", m.group(1)))}">{n}</a></sup>'
        )

    return re.sub(r"<d-footnote>(.*?)</d-footnote>", sub, body, flags=re.S)


def resolve_assets(paths: set[str]) -> dict[str, str]:
    files: dict[str, str] = {}
    for p in sorted(paths):
        m = re.fullmatch(r"assets/(html|img|gif)/submission/([^/]+)", p)
        if not m:
            sys.exit(f"asset path outside the kit layout: {p}")
        hits = [
            d for d in ASSET_DIRS[m.group(1)] if (ROOT / d / m.group(2)).is_file()
        ]
        if len(hits) != 1:
            sys.exit(f"asset {p}: {len(hits)} candidate files ({hits})")
        files[p] = f"{hits[0]}/{m.group(2)}"
    return files


# --------------------------------------------------------------- output


def kit_source(front_raw: str, abstract: str, sections, toc) -> str:
    toc_yaml = ["toc:"] + [
        f"  - name: {json.dumps(name, ensure_ascii=False)}"
        for level, name, _ in toc
        if level == 2
    ]
    styles = f"_styles: >-\n  {KIT_STYLES}"
    header = f"---\n{front_raw}\n" + "\n".join(toc_yaml) + f"\n{styles}\n---"
    parts = [header, abstract]
    parts += [s.raw.strip() for s in sections]
    return "\n\n".join(parts) + "\n"


def page(fm, abstract_html, sections, toc, refs_html, notes_html, counts) -> str:
    css = (SRC / "kit_preview.css").read_text(encoding="utf-8") + KIT_STYLES
    css += (SRC / "demo_extra.css").read_text(encoding="utf-8")
    css += HtmlFormatter(style="friendly").get_style_defs(".highlight")
    nav = [
        f'<div><a href="#{sid}">{html.escape(name)}</a></div>'
        for level, name, sid in toc
        if level == 2
    ]
    body = []
    for s in sections:
        body.append(s.html)
        body.append(
            '<details class="kit-src"><summary>Kit source of this part '
            f"<code>sections/{s.path.name}</code></summary><pre>"
            f"{html.escape(s.raw)}</pre></details>"
        )
    # The builder-written label and the two view toggles sit in the byline, in
    # the kit's own byline style (owner, 2026-10-11: no banner).
    byline_extra = (
        "<div><h3>Submitted</h3><p><em>Not submitted. Demonstration build: "
        "builder-written except the title, abstract and description.</em></p>"
        "</div><div><h3>View</h3>"
        '<p class="view-toggle"><label for="show-notes"><input type="checkbox" '
        f'id="show-notes"> Ledger IDs ({counts["ledger"]})</label></p>'
        '<p class="view-toggle"><label for="show-print"><input type="checkbox" '
        'id="show-print"> Print companions</label></p></div>'
    )
    return f"""<title>CHE Beyond PDF Demo</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Roboto+Mono:wght@400;500&display=swap">
<style>
{css}
</style>
<div class="post distill">
<d-title><h1>{html.escape(fm["title"])}</h1><p>{html.escape(fm["description"])}</p></d-title>
<d-byline><div class="byline grid"><div class="authors-affiliations grid">
<h3>Authors</h3><h3>Affiliations</h3>
<p class="author"><span class="name">Anonymous</span></p>
<p class="affiliation"><span class="affiliation">Anonymous</span></p></div>
{byline_extra}
</div></d-byline>
<d-article>
<d-contents><nav class="l-text figcaption"><h3>Contents</h3>
{"".join(nav)}</nav></d-contents>
<div class="owner-abstract">{abstract_html}</div>
{"".join(body)}
<h2 id="footnotes-and-references">Footnotes and references</h2>
{notes_html}
{refs_html}
</d-article>
</div>
<script>
(function () {{
  var box = document.getElementById("show-notes");
  box.addEventListener("change", function () {{
    document.body.classList.toggle("show-notes", box.checked);
  }});
  var pr = document.getElementById("show-print");
  pr.addEventListener("change", function () {{
    document.body.classList.toggle("show-print", pr.checked);
  }});
}})();
window.MathJax = {{
  tex: {{ inlineMath: [["\\\\(", "\\\\)"]],
         displayMath: [["\\\\[", "\\\\]"]], tags: "ams" }},
  svg: {{ fontCache: "global" }},
  options: {{ skipHtmlTags: ["script", "noscript", "style", "textarea",
                            "pre", "code"] }}
}};
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-svg.js"></script>
"""


def main() -> None:
    fm, front_raw, abstract = read_finale()
    ledger, bib = read_ledgers(), read_bib()
    seen = {"ledger": set(), "missing": set(), "notes": 0}
    assets: set[str] = set()
    sections = [
        Section(p, p.read_text(encoding="utf-8"))
        for p in sorted((DEMO / "sections").glob("*.md"))
    ]
    if not sections:
        sys.exit("no section files")
    for s in sections:
        if HEADER_TAG not in s.raw.split("\n", 1)[0]:
            sys.exit(f"{s.path.name}: first line must carry the {HEADER_TAG} label")
    toc: list = []
    order: list[str] = []
    missing_cites: set[str] = set()
    fns: list[str] = []
    abstract_html = render_markdown(abstract, ledger, seen, assets)
    for s in sections:
        h = render_markdown(s.raw, ledger, seen, assets)
        h = add_heading_ids(h, toc)
        h = citations(h, bib, order, missing_cites)
        s.html = footnotes(h, fns)
    refs = []
    for i, key in enumerate(order, 1):
        e = bib[key]
        venue = e.get("journal") or e.get("booktitle") or e.get("publisher") or ""
        link = e.get("url") or (f"https://doi.org/{e['doi']}" if "doi" in e else "")
        title = html.escape(_distill_tex(e.get("title", "")))
        if link:
            title = f'<a href="{html.escape(link)}">{title}</a>'
        refs.append(
            f'<li id="ref-{key}"><span class="ref-n">[{i}]</span> '
            f"{html.escape(_distill_tex(e.get('author', '')))} ({e.get('year', '')}). "
            f"{title}. <em>{html.escape(_distill_tex(venue))}</em>.</li>"
        )
    refs_html = '<ol class="refs">' + "".join(refs) + "</ol>"
    notes_html = (
        '<ol class="footnotes">'
        + "".join(
            f'<li id="fn-{n}">{t} <a href="#fnref-{n}">↩</a></li>'
            for n, t in enumerate(fns, 1)
        )
        + "</ol>"
        if fns
        else ""
    )
    files = resolve_assets(assets)
    OUT.mkdir(exist_ok=True)
    (DEMO / "submission_demo.md").write_text(
        kit_source(front_raw, abstract, sections, toc), encoding="utf-8"
    )
    counts = {"ledger": len(seen["ledger"]), "notes": seen["notes"]}
    (OUT / "index.html").write_text(
        page(fm, abstract_html, sections, toc, refs_html, notes_html, counts),
        encoding="utf-8",
    )
    (OUT / "files.json").write_text(json.dumps(files, indent=1) + "\n")
    print(f"sections {len(sections)} · headings {len(toc)} · refs {len(order)}")
    print(f"ledger IDs {counts['ledger']} · notes {counts['notes']}", end=" · ")
    print(f"assets {len(files)}")
    if seen["missing"] or missing_cites:
        print(f"UNRESOLVED ledger IDs: {sorted(seen['missing'])}")
        print(f"UNRESOLVED cite keys: {sorted(missing_cites)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
