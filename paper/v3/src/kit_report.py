"""Grade a real-kit build: merge the staging report, the browser measurements and the
printed PDF into ``kit_checks.json`` and a readable ``kit_checks.md`` (called by
``kit_build.sh``; see ``README.md`` for what each check means).

Every check prints PASS, FAIL or INFO with its counts. Exit 1 if any check FAILs.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True  # keep src/ free of __pycache__
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kit_stage import identity_tokens  # noqa: E402

RAW_TEX = re.compile(r"[\\{}$]|--")


def strip_tags(s: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).replace(" ", " ")


def pdf_pages(pdf: Path) -> list[str]:
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(pdf)], capture_output=True,
                                                        text=True).stdout).group(1))
    return [subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), str(pdf), "-"],
                           capture_output=True, text=True).stdout for i in range(1, n + 1)]


def locate(pages: list[str], pdf: Path, phrase: str) -> dict | None:
    """Page and vertical position (fraction of the page height) of a phrase in the PDF."""
    words = phrase.split()[:6]
    if not words:
        return None
    pat = re.compile(r"\s+".join(re.escape(w) for w in words))
    for i, text in enumerate(pages, 1):
        if pat.search(" ".join(text.split())):
            bbox = subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), "-bbox", str(pdf), "-"],
                                  capture_output=True, text=True).stdout
            ph = float(re.search(r'<page width="[\d.]+" height="([\d.]+)"', bbox).group(1))
            for m in re.finditer(r'<word xMin="[\d.]+" yMin="([\d.]+)"[^>]*>([^<]*)</word>', bbox):
                if html.unescape(m.group(2)) == words[0]:
                    frac = float(m.group(1)) / ph
                    return {"page": i, "y_frac": round(frac, 2),
                            "where": "top third" if frac < 1 / 3 else "middle third" if frac < 2 / 3
                            else "bottom third"}
            return {"page": i, "y_frac": None, "where": "?"}
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    for k in ("stage", "browser", "expected", "build-report", "run", "pdf", "zip", "out-json", "out-md"):
        ap.add_argument(f"--{k}", type=Path, required=True)
    ap.add_argument("--max-pages", type=float, default=15.0, help="v3 main-text page ceiling")
    ap.add_argument("--grade", choices=["page1", "section1"], default="page1",
                    help="which main-text reading the page check grades (both are reported)")
    ap.add_argument("--label-pt", type=float, default=8.0, help="nominal figure label size (pt)")
    ap.add_argument("--min-pt", type=float, default=7.0, help="minimum printed label size (pt)")
    a = ap.parse_args()
    st = json.loads(a.stage.read_text(encoding="utf-8"))
    br = json.loads(a.browser.read_text(encoding="utf-8"))
    ex = json.loads(a.expected.read_text(encoding="utf-8"))
    bd = json.loads(a.build_report.read_text(encoding="utf-8"))
    run = json.loads(a.run.read_text(encoding="utf-8"))
    checks: list[dict] = []

    def add(group, name, ok, counts, details=None, info=False):
        status = "INFO" if info else ("PASS" if ok else "FAIL")
        checks.append({"group": group, "check": name, "status": status, "counts": counts,
                       "details": details or []})

    # -- pipeline
    add("Pipeline", "build_v3.py (source checks)", not bd["failures"],
        f"{len(bd['failures'])} failures, {len(bd['warnings'])} warnings, "
        f"{bd['stub_spec_blocks']} STUB-SPEC blocks, {len(bd['m1_flags'])} M1 source flags",
        bd["failures"] + bd["warnings"])
    add("Pipeline", "kit zip sha256", run["sha_ok"], run["sha256"])
    add("Pipeline", "kit merge_files() and jekyll build --future",
        run["merge_rc"] == 0 and run["jekyll_rc"] == 0 and run["control_jekyll_rc"] == 0,
        f"merge {run['merge_rc']}, jekyll {run['jekyll_rc']}, control jekyll {run['control_jekyll_rc']}; "
        f"{run.get('gems', '')}")

    # -- math and Liquid
    m = br["math"]
    add("Math and Liquid", "MathJax errors", m["errors"] == 0,
        f"{m['errors']} errors in {m['rendered']} rendered expressions (source count {ex['math_source']})",
        m["error_texts"])
    add("Math and Liquid", "no raw $ or TeX in rendered text", not br["raw_tex"],
        f"{len(br['raw_tex'])} hits", br["raw_tex"])
    add("Math and Liquid", "math count, source against rendered", True,
        f"source {ex['math_source']}, rendered {m['rendered']}", info=True)
    add("Math and Liquid", "0 Liquid left", br["liquid_left"] == 0, f"{br['liquid_left']} left",
        br["liquid_samples"])

    # -- tables (M1)
    add("Tables (M1)", "kit table count equals the source's", br["tables"] == ex["tables_source"],
        f"kit {br['tables']} against source {ex['tables_source']}; build's M1 source scan flagged "
        f"{len(bd['m1_flags'])} line(s)",
        [f"sections/{f['section']}:{f['line']} [{f['kind']}] {f['text'][:100]}" for f in bd["m1_flags"]]
        + [f"one-row table in the kit page: {x}" for x in br.get("one_row_tables", [])])

    # -- references (M2)
    refs = br["references"]
    raw_hits, mism = [], []
    for r in refs:
        e = ex["bib"].get(r["key"])
        text = strip_tags(r["html"])
        if RAW_TEX.search(text.replace("[link]", "").replace("[PDF]", "").replace("[HTML]", "")):
            raw_hits.append(f"{r['key']}: {text[:140]}")
        if e is None:
            mism.append(f"{r['key']}: rendered but not expected")
            continue
        if (r["title"] or "").strip() != e["title"]:
            mism.append(f"{r['key']}: title shows {r['title']!r}; the field means {e['title']!r}")
        parts = r["html"].split("<br>", 1)
        shown = strip_tags(parts[1]) if len(parts) > 1 else ""
        if e["bib_authors"] and not shown.startswith(e["bib_authors"]):
            mism.append(f"{r['key']}: authors show {shown[:90]!r}; the field means {e['bib_authors'][:90]!r}")
    no_cites = not ex["cited_keys"] and not br["cites"]
    if no_cites:
        add("References (M2)", "references", True, "no <d-cite> in the source, so no reference "
            "list to check (the reference checks run once the text cites)", info=True)
    else:
      add("References (M2)", "no raw LaTeX or -- in Distill's reference list", not raw_hits,
          f"{len(raw_hits)} of {len(refs)} entries", raw_hits)
      add("References (M2)", "rendered authors and titles equal the bib's Unicode fields", not mism and refs,
          f"{len(mism)} mismatches in {len(refs)} entries", mism)
      ref_html = {r["key"]: r["html"].strip() for r in refs}
      unresolved = []
      for c in br["cites"]:
          keys = [k.strip() for k in (c["key"] or "").split(",") if k.strip()]
          no_number = not (c["number"] or "").strip("[] ") or "?" in (c["number"] or "")
          missing = [k for k in keys if k not in ex["bib"] or ref_html.get(k, "?") == "?"]
          if no_number or missing:
              unresolved.append({**c, "missing": missing})
      add("References (M2)", "every d-cite resolves", not unresolved and br["cites"],
          f"{len(br['cites'])} d-cite tags, {len(unresolved)} unresolved",
          [f"{c['key']}: shows {c['number']!r}" + (f"; no bib entry for {c['missing']}" if c["missing"] else "")
           for c in unresolved])
      add("References (M2)", "reference list has one entry per cited key",
          len(refs) == len(ex["cited_keys"]), f"{len(refs)} entries, {len(ex['cited_keys'])} cited keys")
      hover_bad = []
      for c in br["cites"]:
          hv = c["hover"] or ""
          if not re.search(r"<li>", hv):
              hover_bad.append(f"{c['key']}: empty hover card")
          for item in re.findall(r"<li>(.*?)</li>", hv, flags=re.S):
              t = strip_tags(item).replace("[link]", "").replace("[PDF]", "").replace("[HTML]", "")
              if t.strip() == "?":
                  hover_bad.append(f"{c['key']}: a hover entry shows '?' (no bib entry)")
              if RAW_TEX.search(t):
                  hover_bad.append(f"{c['key']}: {t[:120]}")
          items = re.findall(r"<li>(.*?)</li>", hv, flags=re.S)
          keys = [k.strip() for k in (c["key"] or "").split(",")]
          for k, item in zip(keys, items):
              if k not in ex["bib"]:
                  continue
              tt = strip_tags((re.findall(r"<strong>(.*?)</strong>", item, flags=re.S) or [""])[0])
              if tt != ex["bib"][k]["title"]:
                  hover_bad.append(f"{k}: hover title {tt!r}")
              seg = item.split("<br>")
              au = strip_tags(seg[1]).strip() if len(seg) > 1 else ""
              want = ex["bib"][k]["hover_authors"]
              if want and not au.startswith(want):
                  hover_bad.append(f"{k}: hover authors {au[:80]!r}; the field means {want[:80]!r}")
      add("References (M2)", "hover cards show no raw TeX", not hover_bad and br["cites"],
          f"{len(br['cites'])} hover cards, {len(hover_bad)} problems", sorted(set(hover_bad)))

    # -- citation box, byline, title
    ym = re.search(r"year = \{([^}]*)\}", br["cite_box"])
    year = ym.group(1) if ym else ""
    add("Citation box (M3)", "the cite-this-work box has a year", bool(re.search(r"\d{4}", year)),
        f"year = {{{year}}}", [br["cite_box"], br["cite_attribution"]])
    parts = re.split(r"(?i)submitted", br["byline"], maxsplit=1)
    sub = parts[1].strip().split("\n")[0] if len(parts) > 1 else ""
    add("Byline", "what the byline shows for Submitted", True,
        f"{sub!r} (front matter submitted_date: {ex['submitted_date']})", info=True)
    intact = {"h1 equals the title": br["title"] == ex["title"],
              "subtitle equals the description": br["description"] == ex["description"],
              "the byline rendered (Distill parsed the front-matter JSON)": bool(br["byline"].strip()),
              "the cite box carries the title (the layout's script ran)":
                  bool(ex["title"]) and ex["title"] in br["cite_box"]}
    add("Byline", "title and description render intact (heading, byline, cite box)",
        all(intact.values()), f"{sum(intact.values())} of {len(intact)} hold",
        [k for k, v in intact.items() if not v])

    # -- links, frames, images
    toc_bad = [t["name"] for t in br["toc"] if not t["resolves"]]
    add("Links and frames", "every toc link resolves", not toc_bad and len(br["toc"]) == len(ex["toc"]),
        f"{len(br['toc']) - len(toc_bad)} of {len(br['toc'])} resolve (source toc {len(ex['toc'])})", toc_bad)
    anc_bad = [x["href"] for x in br["anchor_links"] if not x["resolves"]]
    add("Links and frames", "every in-page # link resolves", not anc_bad,
        f"{len(br['anchor_links']) - len(anc_bad)} of {len(br['anchor_links'])}", anc_bad)
    fr = br["iframes"]
    not_loaded = [f["src"] for f in fr if not (f["loaded"] and f["same_origin"])]
    add("Links and frames", "every iframe loads (same origin)",
        not not_loaded and len(fr) == ex["iframes_source"],
        f"{len(fr) - len(not_loaded)} of {len(fr)} loaded (source {ex['iframes_source']})", not_loaded)
    # growth and clipping, 5 s and 60 s after load, at three widths (review RM-4)
    grow_bad, clip_bad, height_rows = [], [], []
    settled = {}
    for g in br.get("growth", []):
        for e5, e60 in zip(g["at5"], g["at60"]):
            name = Path(e5["src"] or "").name
            if abs(e60["h"] - e5["h"]) > 1:
                grow_bad.append(f"{g['width']} px: {name} grew from {e5['h']} to {e60['h']} px between 5 s and 60 s")
            if e60["body"] is not None and e60["h"] < e60["body"] - 1:
                clip_bad.append(f"{g['width']} px: {name} frame {e60['h']} px < its document's body {e60['body']} px")
            if e60["body"] is None:
                clip_bad.append(f"{g['width']} px: {name} document not readable (cross-origin or not loaded)")
            height_rows.append(f"{g['width']} px: {name}: frame {e5['h']} → {e60['h']} px, body {e60['body']} px")
            if g["width"] == 1280:
                settled[e5["src"]] = e60["h"]
    widths = [g["width"] for g in br.get("growth", [])]
    add("Links and frames", "iframe heights stable: 5 s and 60 s after load equal (1280, 1024, 390 px)",
        bool(widths) and not grow_bad, f"{len(grow_bad)} frames grew, widths {widths}", grow_bad + height_rows)
    add("Links and frames", "no iframe clips its document: frame ≥ body.scrollHeight at 60 s (1280, 1024, 390 px)",
        bool(widths) and not clip_bad, f"{len(clip_bad)} problems, widths {widths}", clip_bad)
    off, attr_rows = [], []
    for f in fr:
        h = settled.get(f["src"])
        dev = None if not f["attr_height"] or not h else round(100 * (h - f["attr_height"]) / h, 1)
        f["settled_height_1280"], f["attr_deviation_pct"] = h, dev
        attr_rows.append(f"{Path(f['src'] or '').name}: attr {f['attr_height']}, height at 60 s {h} ({dev} %)")
        if dev is not None and abs(dev) > 5:
            off.append(attr_rows[-1])
    add("Links and frames", "iframe height attributes within 5 % of the height at 60 s, 1280 px (P2 §7.2)",
        not off, f"{len(fr) - len(off)} of {len(fr)} within 5 %", off + ["all: " + "; ".join(attr_rows)])
    bad_img = [i["src"] for i in br["images"] if not i["ok"]]
    add("Links and frames", "images load", not bad_img and (br["images"] or not ex["includes_source"]),
        f"{len(br['images']) - len(bad_img)} of {len(br['images'])} (source includes {ex['includes_source']})", bad_img)

    # -- print
    pr = br["print"]
    add("Print", "print companions hidden on screen", all(d == "none" for d in br["companions_screen"]),
        f"{sum(d == 'none' for d in br['companions_screen'])} of {len(br['companions_screen'])} hidden")
    add("Print", "print companions shown in print media, images loaded",
        all(c["display"] != "none" and c["img_ok"] for c in pr["companions"]) and pr["companions"],
        f"{sum(c['display'] != 'none' and c['img_ok'] for c in pr['companions'])} of {len(pr['companions'])}")
    add("Print", "iframes hidden in print media", all(d == "none" for d in pr["iframes"]),
        f"{sum(d == 'none' for d in pr['iframes'])} of {len(pr['iframes'])} hidden")
    po = br.get("print_overflow")
    if po is not None:
        rows = [f"{x['tag']} {x['over_px']} px too wide, under {x['under']!r}: {x['text']}" for x in po["flagged"]]
        if po["article_overflow"] > 1:
            rows.append(f"the article itself overflows by {po['article_overflow']} px")
        wr = po.get("listing_wrapped_lines", [])
        pdf_text = "\n".join(re.sub(r"\s+", " ", ln).strip() for ln in subprocess.run(
            ["pdftotext", "-layout", str(a.pdf), "-"], capture_output=True, text=True).stdout.splitlines())
        broken = [sum(1 for ln in (x.get("text") or "").split("\n")
                      if ln.strip() and re.sub(r"\s+", " ", ln).strip() not in pdf_text)
                  for x in ex["listings"]]
        add("Print", "nothing is cut in print: tables, math and listings fit at US Letter width",
            not po["flagged"] and po["article_overflow"] <= 1,
            f"{len(po['flagged'])} cut of {po['checked']} checked (text column {po['text_column']} px)",
            rows + [f"wrapped listing lines in print (not graded): {wr} (total {sum(wr)}) in print "
                    f"media; listing lines not intact on one line of the printed PDF: {broken} "
                    f"(total {sum(broken)})"])
    if pr["interact"]:
        add("Print", "'Interact' notes hidden in print", all(d == "none" for d in pr["interact"]),
            f"{sum(d == 'none' for d in pr['interact'])} of {len(pr['interact'])}")

    # -- requests
    loaded_frames = {f["src"] for f in br["iframes"] if f["loaded"]}
    failed = [x for x in br["requests"]["failed"]
              if not ("ERR_ABORTED" in x["why"] and any(x["url"].endswith(s) for s in loaded_frames))]
    add("Requests", "0 failed requests", not failed,
        f"{len(failed)} failed of {br['requests']['total']}"
        f" ({br['requests'].get('aborted_then_loaded', 0) + len(br['requests']['failed']) - len(failed)}"
        " aborted during re-layout and then loaded, not counted)",
        [f"{x['url'][:120]} ({x['why']})" for x in failed])
    add("Requests", "console errors", True, f"{len(br['console_errors'])} console, "
        f"{len(br['page_errors'])} page errors", br["console_errors"] + br["page_errors"], info=True)

    # -- listings and overflow
    exl = [x for x in ex["listings"]]
    lst_bad = []
    for n, x in enumerate(exl):
        got = br["listings"][n] if n < len(br["listings"]) else None
        if got is None:
            lst_bad.append(f"listing {n + 1} ({x['path']}): not in the built page")
            continue
        got = got[:-1] if got.endswith("\n") else got
        lines = got.split("\n")
        if x.get("header"):
            if lines[0] != x["header"]:
                lst_bad.append(f"listing {n + 1}: header line {lines[0]!r}")
            lines = lines[1:]
        if x.get("text") is None or "\n".join(lines) != x["text"]:
            lst_bad.append(f"listing {n + 1} ({x['path']}:{x['start']}-{x['end']}): built text differs "
                           "from the committed lines")
    if len(br["listings"]) != len(exl):
        lst_bad.append(f"{len(br['listings'])} code blocks in the page, {len(exl)} listings in the source")
    add("Listings and overflow", "listings in the built page equal their committed lines byte for byte",
        not lst_bad, f"{len(exl) - len([b for b in lst_bad if b.startswith('listing')])} of {len(exl)} identical",
        lst_bad)
    ov_rows, ov_fail = [], []
    for w in ("1024", "1280", "390"):
        o = br["overflow"][w]
        cut = [i + 1 for i, p in enumerate(o["listings"]) if p["scroll"] > p["client"]]
        worst = max([p["scroll"] - p["client"] for p in o["listings"]] or [0])
        page_over = o["page_scroll_width"] - o["inner_width"]
        ov_rows.append(f"{w} px: listings scrolling inside their block {cut or 'none'} (worst {worst} px); "
                       f"page horizontal overflow {max(0, page_over)} px"
                       + (f"; wide elements {o['widest'][:4]}" if page_over > 0 else ""))
        if w in ("1024", "1280") and cut:
            ov_fail.append(ov_rows[-1])
        if page_over > 0:
            ov_fail.append(ov_rows[-1])
    add("Listings and overflow", "no listing cut at 1024 or 1280 px; no page overflow at any width",
        not ov_fail, f"listing font {br['listing_font']}", ov_rows)
    wm_rows = []
    for w in ("1024", "1280", "390"):
        for x in br["overflow"][w].get("wide_math", []):
            wm_rows.append(f"{w} px: display math {x['over_px']} px too wide, "
                           f"{'scrolls' if x['scrolls'] else 'CUT OFF (no scrollbar)'}, under "
                           f"{x['under']!r}: {x['tex']!r}")
    cut_math = [r for r in wm_rows if "CUT OFF" in r]
    add("Listings and overflow", "display math wider than the column (reported, not graded)", True,
        f"{len(wm_rows)} instances over three widths, {len(cut_math)} cut off with no scrollbar",
        wm_rows, info=True)

    # -- footnote (N1)
    pages = pdf_pages(a.pdf)
    fn_rows = []
    for k, f in enumerate(br["footnotes"]):
        where_text = locate(pages, a.pdf, f["text"])
        ctx = ex["footnote_context"][k] if k < len(ex["footnote_context"]) else ""
        where_marker = locate(pages, a.pdf, " ".join(ctx.split()[-4:])) if ctx else None
        fl = br["footnote_list"] or {}
        fn_rows.append(
            f"footnote {k + 1} ({f['text'][:60]}…): on screen the marker is at {f['marker_frac']:.1%} of the "
            f"page height, under {f['under_heading']!r}; its text is listed in the footnote list at "
            f"{fl.get('frac', 0):.1%} (inside d-appendix: {fl.get('in_appendix')}). Printed PDF "
            f"({len(pages)} pages): the marker's sentence is on page "
            f"{where_marker['page'] if where_marker else '?'}; the footnote TEXT is on page "
            f"{where_text['page'] if where_text else 'not found'}"
            f"{', ' + where_text['where'] if where_text else ''}.")
    ab = locate(pages, a.pdf, ex.get("abstract_start", ""))
    first = " ".join(pages[0].split())[:160] if pages else ""
    fn_rows.append(f"Printed page 1 holds: {first!r} … The abstract starts on page "
                   f"{ab['page'] if ab else 'not found'}.")
    add("Footnote (N1)", "where <d-footnote> text lands, on screen and in print", True,
        f"{len(br['footnotes'])} footnote(s)" if br["footnotes"] else "no <d-footnote> in the source",
        fn_rows, info=True)

    # -- v3 main text (V3-S1, S2, S3, S5; P2's print legibility). Source-side results come
    # from build_v3.py (build_report.json "v3_checks"); pages and legibility are measured on
    # the printed PDF here.
    import v3_checks as v3  # noqa: E402
    v3c = bd.get("v3_checks") or {}
    heads = {"end_heading": v3c.get("end_heading"), "start_heading": v3c.get("start_heading")}
    pg = v3.run_pages(a.pdf, heads["end_heading"], heads["start_heading"], a.max_pages, a.grade)
    add("v3 main text", f"main-text printed pages <= {a.max_pages:g} (graded reading: "
        f"{'from page 1' if a.grade == 'page1' else 'from the first numbered H2'})", pg["status"] == "PASS",
        f"from page 1 {pg['from_page1']}; from {pg['start_heading']!r} {pg['from_section1']}; "
        f"to {pg['end_heading']!r} (PDF {pg['pages_in_pdf']} pages)",
        [f"end heading at {pg['end']}", f"first numbered H2 at {pg['start']}"] + pg["notes"])
    vt = v3c.get("terms", {"status": "NOT CONFIGURED"})
    if vt["status"] == "NOT CONFIGURED":
        add("v3 main text", "no internal code or private-vocabulary term", True, "no term list", info=True)
    else:
        add("v3 main text", "no internal code or private-vocabulary term (appendix exempt)",
            vt["status"] == "PASS",
            f"{len(vt['hits'])} hits; {vt['terms']} terms ({vt['list']}); "
            f"{len(vt['exempt_registered'])} registered-exempt, {len(vt['glossed'])} glossed, "
            f"{len(vt['in_code_not_graded'])} in listings (not graded)",
            [f"{h['where']} {h['match']!r} ({h['term']}): {h['context']}" for h in vt["hits"]]
            + [f"parse: {x}" for x in vt.get("problems", [])])
    sd = v3c.get("dates", {"status": "NOT CONFIGURED", "hits": [], "allowed": []})
    add("v3 main text", "no date outside the allow-list (appendix exempt)", sd["status"] == "PASS",
        f"{len(sd['hits'])} dates outside the allow-list; {len(sd.get('allowed', []))} allowed "
        f"({sd.get('list')})",
        [f"{h['where']} {h['match']!r} [{h['kind']}]: {h['context']}" for h in sd["hits"]])
    sc = v3c.get("caveats", {"status": "NOT CONFIGURED"})
    if sc["status"] == "NOT CONFIGURED":
        add("v3 main text", "each caveat in its one home", True, f"no map ({sc.get('list')})", info=True)
    else:
        rows = []
        for r in sc["caveats"]:
            if r["status"] == "FAIL":
                rows += [f"{r['id']} {r.get('name', '')}: {x}" for x in r["problems"]]
                rows += [f"{r['id']} {r.get('name', '')}: {v['where']} ({v['why']}): {v['text'][:200]}"
                         for v in r["violations"]]
        add("v3 main text", "each caveat in its one home (one-home map)", sc["status"] == "PASS",
            f"{sc['failing']} of {len(sc['caveats'])} entries fail ({sc['list']})",
            rows + [f"parse: {x}" for x in sc.get("problems", [])])
    mk = bd.get("markers") or {}
    add("v3 main text", "HOLE:INTERACTION and OWNER-PENDING markers (reported until step 0.5 and the owner's rulings)",
        True, f"{len(mk.get('HOLE:INTERACTION', []))} HOLE:INTERACTION, {len(mk.get('OWNER-PENDING', []))} OWNER-PENDING; "
        f"{len(bd.get('pending_ledger_tags', []))} tags on PENDING ledger rows",
        [f"{k} {w}" for k, v in mk.items() for w in v] + [f"PENDING row: {x}" for x in bd.get("pending_ledger_tags", [])],
        info=True)
    out_dir = a.build_report.parent
    lg = v3.run_legibility(a.pdf, (out_dir / bd.get("kit_source", "submission_v3.md")).read_text(encoding="utf-8"),
                           json.loads((out_dir / "files.json").read_text(encoding="utf-8")),
                           a.label_pt, a.min_pt, pg["end"]["page"] if pg.get("end") else None)
    add("v3 main text", f"figure images legible in print: a {a.label_pt:g} pt label prints at >= "
        f"{a.min_pt:g} pt (estimate)", lg["status"] in ("PASS", "EMPTY"),
        f"{lg['failing']} of {len(lg['images'])} printed images fail",
        [f"{r['status']} p{r['pdf_page']} {Path(r.get('source') or '?').name}: printed {r['printed_in']} in, "
         f"drawn {r.get('source_in', '?')} in, label {r.get('label_pt_printed', '?')} pt"
         + (f" ({r['why']})" if r.get("why") else "") for r in lg["images"]])

    # -- YAML, stripping, leaks, outputs
    y = st["yaml"]
    add("YAML", "title and description: one line, no double quote, YAML-safe", y["status"] == "PASS",
        "staged front matter parses; " + ("no problems" if not y["problems"] else f"{len(y['problems'])} problems"),
        y["problems"])
    c = st["comments"]
    add("Leaks and print", "comment-stripped staged submission.md (M4)", c["status"] == "PASS",
        f"{c['in_source']} comments in {bd.get('kit_source', 'submission_v3.md')} ({c['stub_spec_in_source']} STUB-SPEC), "
        f"{c['left_in_staged']} '<!--' left in the staged copy")
    b = st["bib"]
    if b.get("parse_error"):
        add("References (M2)", "the bib parses with the kit's parser rules", False,
            f"bibtexParse would throw: {b['parse_error']}")
    add("Leaks and print", "staged bib has no % lines (N3)", b["status"] == "PASS",
        f"{b['percent_lines_in_source']} % lines in the bib, {b['percent_lines_staged']} staged; "
        f"{b['entries']} entries")
    ct = br.get("control")
    if ct:
        same = ct["same_text"] and ct["tables"][0] == ct["tables"][1] and ct["math"][0] == ct["math"][1]
        add("Leaks and print", "stripping removed only comments (stripped build = unstripped build)", same,
            f"rendered text {'identical' if ct['same_text'] else 'DIFFERS'} ({ct['stripped_len']} chars); "
            f"tables {ct['tables']}; math {ct['math']}; listings {ct['listings']}",
            [json.dumps(ct["first_difference"], ensure_ascii=False)] if ct["first_difference"] else [])
    lk = st["leaks"]
    det = [f"{k}: {v}" for k, vs in lk["hits"].items() for v in vs]
    add("Leaks and print", "double-blind grep of the staged folder", lk["status"] == "PASS",
        f"{lk['files']} files; {lk['tokens_checked']} identity tokens; "
        + ", ".join(f"{k} {len(v)}" for k, v in lk["hits"].items()), det)
    info = subprocess.run(["pdfinfo", str(a.pdf)], capture_output=True, text=True).stdout
    size = re.search(r"Page size:\s+(.*)", info)
    letter = bool(size and "612 x 792" in size.group(1))
    all_text = "\n".join(pages).lower()
    pdf_hits = [f"identity token #{n} ({lab})" for n, (lab, t) in enumerate(identity_tokens(), 1)
                if t.lower() in all_text]
    pdf_hits += [m.group(0) for m in re.finditer(r"/(?:home|root|tmp|users)/\S+", all_text)][:5]
    add("Leaks and print", "printed PDF written (US Letter), no identity strings in its text",
        a.pdf.exists() and letter and not pdf_hits,
        f"{len(pages)} pages, {a.pdf.stat().st_size / 1e6:.1f} MB, page size {size.group(1) if size else '?'}",
        pdf_hits)
    with zipfile.ZipFile(a.zip) as z:
        names = z.namelist()
    tops = sorted({n.split("/")[0] for n in names})
    md_in_zip = [n for n in names if n.endswith("submission.md")]
    add("Leaks and print", "staged folder zipped", tops == ["submission_folder"] and md_in_zip,
        f"{len(names)} entries, top level {tops}, {a.zip.stat().st_size / 1e6:.1f} MB")

    # never echo an identity string or a full hash into a report
    toks = identity_tokens()

    def mask(s: str) -> str:
        for n, (_, tok) in enumerate(toks, 1):
            s = re.sub(re.escape(tok), f"[identity #{n}]", s, flags=re.I)
        return re.sub(r"\b([0-9a-f]{4})[0-9a-f]{12,}\b", r"\1…", s)

    for c in checks:
        c["counts"] = mask(str(c["counts"]))
        c["details"] = [mask(str(d)) for d in c["details"]]
    n_fail = sum(1 for c in checks if c["status"] == "FAIL")
    summary = {"pass": sum(1 for c in checks if c["status"] == "PASS"), "fail": n_fail,
               "info": sum(1 for c in checks if c["status"] == "INFO")}
    result = {"summary": summary, "run": run, "checks": checks, "iframes": fr, "growth": br.get("growth"),
              "v3_pages": pg, "v3_legibility": lg,
              "print_overflow": br.get("print_overflow"),
              "overflow": br["overflow"], "footnotes": br["footnotes"]}
    a.out_json.write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    md = ["# Real-kit build checks", "",
          f"Generated by `kit_build.sh` (`kit_report.py`). Source: `{bd['root']}` "
          f"({bd['mode']} build, bib `{bd['bib']}`). Kit sha256 `{run['sha256'][:8]}…{run['sha256'][-7:]}` "
          f"({'verified' if run['sha_ok'] else 'MISMATCH'}); {run.get('gems', '')}. "
          f"Run directory (scratch): `{run['run_name']}`.", "",
          f"**{summary['pass']} PASS, {summary['fail']} FAIL, {summary['info']} INFO.**", "",
          "| group | check | result | counts |", "|---|---|---|---|"]
    for c in checks:
        md.append(f"| {c['group']} | {c['check']} | **{c['status']}** | {c['counts'].replace('|', '/')} |")
    md += ["", "## Details", ""]
    for c in checks:
        if c["details"]:
            md.append(f"### {c['check']} ({c['status']})")
            md.append("")
            md += [f"- {str(d).replace(chr(10), ' ')[:700]}" for d in c["details"][:60]]
            if len(c["details"]) > 60:
                md.append(f"- … {len(c['details']) - 60} more in kit_checks.json")
            md.append("")
    a.out_md.write_text("\n".join(md) + "\n", encoding="utf-8")
    for c in checks:
        print(f"{c['status']:4}  {c['group']}: {c['check']} — {c['counts']}")
    print(f"kit checks: {summary['pass']} PASS, {summary['fail']} FAIL, {summary['info']} INFO")
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
