"""Word counts, one way for every writer (paper_v3_prompt.md, "Count words one way: P3's
method, everywhere").

Planner P3's script (Paper v3 step 1, scratch ``P3/wordcount.py``), a re-implementation
of v2 ``plans/P3.md`` §5's method, copied by builder B2 with its counting function
unchanged. Per section file: prose words, caption words, figure-note words, table words
and code lines. HTML comments, fenced code, math and Liquid are dropped; a word is a
whitespace token holding a letter or digit; markdown-it (commonmark + tables) decides
what is prose, heading, table or HTML. Headings are parsed but not printed, as in P3.

    $PY paper/v3/src/wordcount.py [SECTIONS_DIR]     # default paper/v3/sections
"""

import glob
import os
import re
import sys

from markdown_it import MarkdownIt

sys.dont_write_bytecode = True

md = MarkdownIt("commonmark").enable("table")


def words(s):
    return [w for w in s.split() if re.search(r"[A-Za-z0-9]", w)]


def count(path):
    t = open(path, encoding="utf-8").read()
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    code = 0

    def fc(m):
        nonlocal code
        code += m.group(0).count("\n")
        return ""

    t = re.sub(r"```.*?```", fc, t, flags=re.S)
    caps = []
    notes = []
    for m in re.finditer(r'<span class="figure-note"[^>]*>(.*?)</span>', t, flags=re.S):
        notes.append(m.group(1))
    t = re.sub(r'<span class="figure-note"[^>]*>.*?</span>', "", t, flags=re.S)
    for pat in [
        r"<figcaption[^>]*>(.*?)</figcaption>",
        r'<p class="caption"[^>]*>(.*?)</p>',
        r'caption="([^"]*)"',
    ]:
        caps += re.findall(pat, t, flags=re.S)
        t = re.sub(pat, "", t, flags=re.S)
    t = re.sub(r"\$\$.*?\$\$", "", t, flags=re.S)
    t = re.sub(r"\$[^$\n]*\$", "", t)
    t = re.sub(r"\{%.*?%\}", "", t, flags=re.S)
    toks = md.parse(t)
    prose = 0
    head = 0
    tab = 0
    ctx = []
    for tk in toks:
        if tk.type.endswith("_open"):
            ctx.append(tk.type[:-5])
        elif tk.type.endswith("_close"):
            ctx and ctx.pop()
        elif tk.type == "inline":
            c = re.sub(r"<[^>]+>", " ", tk.content)
            n = len(words(c))
            if "table" in ctx:
                tab += n
            elif "heading" in ctx:
                head += n
            else:
                prose += n
        elif tk.type == "html_block":
            c = re.sub(r"<[^>]+>", " ", tk.content)
            prose += len(words(c))
    capw = sum(len(words(re.sub(r"<[^>]+>", " ", c))) for c in caps)
    notew = sum(len(words(re.sub(r"<[^>]+>", " ", c))) for c in notes)
    return prose, capw, notew, tab, code


def main() -> None:
    d = (
        sys.argv[1]
        if len(sys.argv) > 1
        else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sections")
    )
    tot = [0, 0, 0, 0, 0]
    print("file prose captions notes tables code_lines")
    for p in sorted(glob.glob(os.path.join(d, "*.md"))):
        c = count(p)
        tot = [a + b for a, b in zip(tot, c, strict=True)]
        print(os.path.basename(p), *c)
    print("TOTAL", *tot)


if __name__ == "__main__":
    main()
