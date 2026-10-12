"""Stage the kit's ``submission_folder/`` from a v2 build, and run the checks that need
no browser (called by ``kit_build.sh``; see ``README.md``).

Reads ``<root>/out/submission_v2.md``, ``files.json`` and ``build_report.json`` (written by
``build_v2.py``) and the v2 bib. Writes, under ``--stage`` (a new, empty directory):

- ``submission_folder/submission.md``: the kit source with EVERY HTML comment removed
  (M4): ledger tags, the line-1 status comments and STUB-SPEC blocks. A comment that fills
  its lines is removed with them, so no blank line splits a paragraph; others are cut out
  of their line. Fenced code is never touched, and the staged file must hold 0 ``<!--``;
- ``submission_folder/assets/bibliography/submission.bib``: the bib with its ``%`` lines
  removed (N3: the bib is public);
- ``submission_folder/assets/{html,img,gif}/submission/*``: the assets of ``files.json``.

Also writes ``--control-md`` (the unstripped source, for the stripped-vs-unstripped
comparison), ``--expected`` (what the browser checks compare against) and ``--report``
(the YAML check, the stripping counts and a double-blind scan of the staged folder).
Identity strings for the scan come from this repository's git config and remote at run
time and are never written out; hits are reported masked.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

sys.dont_write_bytecode = True  # keep src/ free of __pycache__
sys.path.insert(0, str(Path(__file__).resolve().parent))
import distill_port as dp  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
FENCE = re.compile(r"(?ms)^ {0,3}(`{3,}|~{3,}).*?^ {0,3}\1[ \t]*$")
NOT_END = r"(?:(?!-->).)*"


def strip_comments(text: str) -> tuple[str, int]:
    """Remove HTML comments outside fenced code; return (text, comments removed)."""
    store: list[str] = []

    def keep(m):
        store.append(m.group(0))
        return f"\x00FENCE{len(store) - 1}\x00"

    body = FENCE.sub(keep, text)
    n = len(re.findall(r"<!--", body))
    body = re.sub(rf"(?m)^[ \t]*<!--{NOT_END}-->[ \t]*\n", "", body, flags=re.S)
    body = re.sub(rf"[ \t]*<!--{NOT_END}-->(?=[ \t]*$)", "", body, flags=re.S | re.M)
    body = re.sub(rf"<!--{NOT_END}-->", "", body, flags=re.S)
    body = re.sub(r"\x00FENCE(\d+)\x00", lambda m: store[int(m.group(1))], body)
    return body, n


def split_front_matter(text: str) -> tuple[str, str]:
    """Exactly as the kit's compile_submission.py splits it."""
    m = re.compile(r"^(---\s*\n.*?\n---\s*\n)(.*)", re.S).match(text)
    return (m.group(1), m.group(2)) if m else ("", text)


def yaml_check(md: str) -> dict:
    fm_text, _ = split_front_matter(md)
    res = {"status": "PASS", "problems": [], "fields": {}}
    try:
        fm = yaml.safe_load(fm_text.strip().strip("-")) or {}
    except yaml.YAMLError as e:
        return {"status": "FAIL", "problems": [f"front matter does not parse: {e}"], "fields": {}}
    for key in ("title", "description"):
        v = fm.get(key)
        res["fields"][key] = v
        if not isinstance(v, str) or not v:
            res["problems"].append(f"{key} missing or not a string")
            continue
        if '"' in v:
            res["problems"].append(f"{key} contains a double quote")
        if "\\" in v:
            res["problems"].append(f"{key} contains a backslash")
        if "\n" in v:
            res["problems"].append(f"{key} is not one line")
        if "</script" in v.lower():
            res["problems"].append(f"{key} contains </script")
    for name in [t.get("name", "") for t in fm.get("toc") or []]:
        if '"' in name:
            res["problems"].append(f"toc name {name!r} contains a double quote")
    if fm.get("layout") != "distill":
        res["problems"].append("layout is not distill")
    if fm.get("bibliography") != "submission.bib":
        res["problems"].append("bibliography is not submission.bib")
    if "openreview_id" in fm:
        res["problems"].append("openreview_id is set")
    for a in fm.get("authors") or []:
        if a.get("name") != "Anonymous" or "url" in a:
            res["problems"].append(f"author not anonymous: {a}")
    for key in ("date", "submitted_date"):
        res["fields"][key] = str(fm[key]) if key in fm else None
    if res["problems"]:
        res["status"] = "FAIL"
    return res


TOOL_IDENTITY = re.compile(r"claude|anthropic", re.I)   # the disclosure names the tool


def identity_tokens() -> list[tuple[str, str]]:
    """(label, token) pairs that would identify the author: every commit author's name, name
    words and e-mail (git log), git config's name and e-mail, the remote's owner and
    repository names, the repository directory, and KIT_IDENTITY_EXTRA (comma-separated).
    Tool identities (Claude, Anthropic) are left out, because the disclosure footnote names
    the tool. Read at run time and never printed: reports show 'identity token #n'."""
    import os
    toks = []

    def git(*a):
        try:
            return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True,
                                  text=True, check=True).stdout.strip()
        except subprocess.CalledProcessError:
            return ""

    people = set(git("log", "--format=%an%x09%ae").splitlines())
    people.add(git("config", "user.name") + "\t" + git("config", "user.email"))
    for line in sorted(people):
        name, _, email = line.partition("\t")
        if TOOL_IDENTITY.search(line):
            continue
        if name:
            toks.append(("commit author name", name))
            toks += [("commit author name word", w) for w in name.split() if len(w) >= 4]
        if email:
            toks.append(("commit author e-mail", email))
            toks.append(("commit author e-mail local part", email.split("@")[0]))
    url = git("remote", "get-url", "origin")
    m = re.search(r"[:/]([^/:]+)/([^/]+?)(?:\.git)?$", url)
    if m:
        toks.append(("remote owner", m.group(1)))
        toks.append(("remote repository", m.group(2)))
        toks.append(("remote repository (hyphens)", m.group(2).replace("_", "-")))
    toks.append(("repository directory", ROOT.name))
    toks += [("KIT_IDENTITY_EXTRA", x.strip()) for x in os.environ.get("KIT_IDENTITY_EXTRA", "").split(",")
             if x.strip()]
    seen, out = set(), []
    for label, t in toks:
        if len(t) >= 4 and t.lower() not in seen and not TOOL_IDENTITY.search(t):
            seen.add(t.lower())
            out.append((label, t))
    return out


def resolves_in_repo(h: str) -> bool:
    return subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", h],
                          capture_output=True).returncode == 0


def leak_scan(folder: Path, bib_urls: set[str]) -> dict:
    """Double-blind grep of the staged folder: URLs that are not a cited work's or a
    namespace URI, identity strings, absolute paths, hex hashes of 7+ characters, and
    text chunks in images."""
    tokens = identity_tokens()
    hits = {"url": [], "identity": [], "abs_path": [], "hex": [], "image_text": []}
    allowed_url = re.compile(r"^https?://www\.w3\.org/")
    for p in sorted(folder.rglob("*")):
        if not p.is_file():
            continue
        relp = str(p.relative_to(folder))
        data = p.read_bytes()
        if p.suffix.lower() in (".png",):
            for chunk in (b"tEXt", b"iTXt", b"zTXt", b"eXIf"):
                if chunk in data:
                    hits["image_text"].append(f"{relp}: PNG {chunk.decode()} chunk")
            continue
        if p.suffix.lower() in (".gif", ".jpg", ".jpeg", ".webp"):
            if b"\x21\xfe" in data:
                hits["image_text"].append(f"{relp}: GIF comment extension")
            continue
        text = data.decode("utf-8", errors="replace")
        scan = re.sub(r"data:[\w/+.-]+;base64,[A-Za-z0-9+/=]+", "data:BASE64", text)
        for m in re.finditer(r"https?://[^\s\"'<>)\]}]+", scan):
            u = m.group(0).rstrip(".,;")
            if allowed_url.match(u):
                continue
            if p.suffix == ".bib" and u in bib_urls:
                continue
            hits["url"].append(f"{relp}: {u}")
        low = scan.lower()
        for n, (label, tok) in enumerate(tokens, 1):
            c = low.count(tok.lower())
            if c:
                hits["identity"].append(f"{relp}: identity token #{n} ({label}) x{c}")
        for m in re.finditer(r"(?<![\w.~-])(/(?:home|root|tmp|Users|opt|mnt|var|etc|srv)/[^\s\"'<>)]*"
                             r"|[A-Za-z]:\\\\[^\s\"'<>]*)", scan):
            hits["abs_path"].append(f"{relp}: {m.group(0)[:60]}")
        for m in re.finditer(r"(?<![0-9A-Za-z])(?=[0-9a-f]*[a-f])(?=[0-9a-f]*[0-9])[0-9a-f]{7,}"
                             r"(?![0-9A-Za-z])", scan):
            h = m.group(0)
            ctx = scan[max(0, m.start() - 25):m.end() + 10].replace("\n", " ")
            hits["hex"].append(f"{relp}: {h}{' (RESOLVES in this repository)' if resolves_in_repo(h) else ''}"
                               f" … {ctx!r}")
    n = sum(len(v) for v in hits.values())
    return {"status": "PASS" if n == 0 else "FAIL", "hits": hits, "tokens_checked": len(tokens),
            "files": sum(1 for p in folder.rglob("*") if p.is_file())}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--bib", type=Path, required=True)
    ap.add_argument("--stage", type=Path, required=True, help="new, empty directory")
    ap.add_argument("--control-md", type=Path, required=True)
    ap.add_argument("--expected", type=Path, required=True)
    ap.add_argument("--report", type=Path, required=True)
    a = ap.parse_args()
    out = a.root / "out"
    src = (out / "submission_v2.md").read_text(encoding="utf-8")
    files = json.loads((out / "files.json").read_text(encoding="utf-8"))
    build = json.loads((out / "build_report.json").read_text(encoding="utf-8"))
    if a.stage.exists() and any(a.stage.iterdir()):
        sys.exit(f"{a.stage} is not empty")
    folder = a.stage / "submission_folder"
    (folder / "assets" / "bibliography").mkdir(parents=True)

    stripped, n_comments = strip_comments(src)
    (folder / "submission.md").write_text(stripped, encoding="utf-8")
    a.control_md.write_text(src, encoding="utf-8")
    bib_text = a.bib.read_text(encoding="utf-8")
    bib_lines = bib_text.splitlines()
    kept = [ln for ln in bib_lines if not ln.lstrip().startswith("%")]
    staged_bib = "\n".join(kept).lstrip("\n") + "\n"
    (folder / "assets" / "bibliography" / "submission.bib").write_text(staged_bib, encoding="utf-8")
    for pub, rp in files.items():
        dst = folder / pub
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rp, dst)

    try:
        raw = dp.parse_bib(bib_text, normalize=False)
        bib_error = None
    except dp.BibParseError as e:     # the kit's parser would throw too: build anyway, grade later
        raw, bib_error = {}, str(e)
        raw = {f"_url{i}": {"url": u} for i, u in
               enumerate(re.findall(r"\burl\s*=\s*\{([^}]*)\}", bib_text, flags=re.I))}
    bib_urls = {v.get("url", "") for v in raw.values()} | {f"https://doi.org/{v['doi']}"
                                                           for v in raw.values() if "doi" in v}
    report = {
        "comments": {"in_source": len(re.findall(r"<!--", src)), "removed": n_comments,
                     "left_in_staged": stripped.count("<!--"),
                     "stub_spec_in_source": len(re.findall(r"<!--\s*STUB-SPEC", src)),
                     "status": "PASS" if stripped.count("<!--") == 0 and "-->" not in stripped
                     else "FAIL"},
        "bib": {"percent_lines_in_source": len(bib_lines) - len(kept),
                "percent_lines_staged": sum(1 for ln in staged_bib.splitlines()
                                            if ln.lstrip().startswith("%")),
                "entries": 0 if bib_error else len(raw), "parse_error": bib_error},
        "yaml": yaml_check(stripped),
        "assets": len(files),
        "leaks": leak_scan(folder, bib_urls),
    }
    report["bib"]["status"] = "PASS" if report["bib"]["percent_lines_staged"] == 0 else "FAIL"
    a.report.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    exp_bib = {}
    for key in build.get("cited_keys_in_order", []):
        if key not in raw:
            continue
        meant = {k: dp.tex_to_unicode(v) for k, v in raw[key].items() if k != "type"}
        exp_bib[key] = {"title": meant.get("title", ""),
                        "bib_authors": dp.author_string(meant, "${L}, ${I}", ", ", " and "),
                        "hover_authors": dp.author_string(meant, "${I} ${L}", ", ")}
    fm = report["yaml"]["fields"]
    footnotes = [re.sub(r"<[^>]+>", "", f["text"]).strip() for f in build.get("footnotes", [])]
    first_para = next((b for b in re.split(r"\n\s*\n", split_front_matter(stripped)[1]) if b.strip()), "")
    abstract_start = " ".join(re.sub(r"<[^>]+>|\$[^$]*\$|[*_`]", " ", first_para).split()[:6])
    contexts = []
    for m in re.finditer(r"<d-footnote>", stripped):
        before = re.sub(r"<[^>]+>|\$[^$]*\$|[*_`]", " ", stripped[max(0, m.start() - 400):m.start()])
        contexts.append(" ".join(before.split()[-6:]))
    expected = {
        "title": fm.get("title"), "description": fm.get("description"),
        "date": fm.get("date"), "submitted_date": fm.get("submitted_date"),
        "byline_submitted": build.get("byline_submitted"),
        "tables_source": build["tables_source"]["total"],
        "math_source": build.get("math_source"),
        "toc": [t["name"] for t in build.get("toc", [])],
        "cited_keys": build.get("cited_keys_in_order", []),
        "bib": exp_bib,
        "listings": [{"path": x.get("path"), "start": x.get("start"), "end": x.get("end"),
                      "header": x.get("header"), "text": x.get("text")}
                     for x in build.get("listings", [])],
        "footnotes": footnotes,
        "footnote_context": contexts,
        "abstract_start": abstract_start,
        "iframes_source": len(re.findall(r"<iframe\b", stripped)),
        "includes_source": build["liquid"]["include"],
    }
    a.expected.write_text(json.dumps(expected, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"staged {folder}: {n_comments} comments removed, "
          f"{report['comments']['left_in_staged']} left; bib % lines "
          f"{report['bib']['percent_lines_in_source']} -> {report['bib']['percent_lines_staged']}; "
          f"{len(files)} assets; YAML {report['yaml']['status']}; "
          f"double-blind scan {report['leaks']['status']}")


if __name__ == "__main__":
    main()
