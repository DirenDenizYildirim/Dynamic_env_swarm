"""Self-tests of the v3 main-text checks (builder B2): each check FAILS on Paper v2's text or
printed PDF (the negative controls, recorded in ``VALIDATION.md``) and PASSES on a minimal
positive fixture. Not part of the project's CPU suite (``testpaths = che/tests``); run:

    PYTHONDONTWRITEBYTECODE=1 $PY -m pytest -p no:cacheprovider paper/v3/src/tests -q

Needs pyyaml, Pillow, matplotlib and poppler (``pdftotext``, ``pdfimages``).
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True  # keep src/ free of __pycache__
sys.path.insert(0, str(SRC))
import v3_checks as vc  # noqa: E402

ROOT = SRC.parents[2]
V2 = ROOT / "paper" / "v2"
POS = SRC / "fixtures" / "pos"
V2_PDF = V2 / "out" / "submission_v2_print.pdf"
B1_TERMS = ROOT / "paper" / "v3" / "checks" / "terms.txt"
SEED_TERMS = SRC / "checks_seed" / "terms.seed.txt"
B1_DATES = ROOT / "paper" / "v3" / "checks" / "dates_allow.txt"
NEED_POPPLER = pytest.mark.skipif(
    shutil.which("pdftotext") is None, reason="poppler missing"
)


# ------------------------------------------------------------ negative controls (v2)


@pytest.mark.parametrize("terms", [B1_TERMS, SEED_TERMS])
def test_terms_fail_on_v2(terms):
    if not terms.exists():
        pytest.skip(f"{terms} not written yet")
    res = vc.terms_check(V2, terms)
    assert res["status"] == "FAIL"
    assert (
        sum(1 for h in res["hits"] if "GPU" in h["term"]) >= 17
    )  # P3 §5.2: GPU 1/2/3 (17)


def test_dates_fail_on_v2():
    res = vc.dates_check(
        V2,
        B1_DATES if B1_DATES.exists() else SRC / "checks_seed" / "dates_allow.seed.txt",
    )
    assert res["status"] == "FAIL"
    iso = [h for h in res["hits"] + res["allowed"] if h["kind"] == "iso"]
    assert len(iso) == 21  # P3 §5.2 and B1: 21 ISO dates


def test_caveats_fail_on_v2():
    res = vc.caveats_check(V2, SRC / "fixtures" / "caveats_v2_negcontrol.yaml")
    assert res["status"] == "FAIL"
    twice = next(c for c in res["caveats"] if c["id"].startswith("DES-14"))
    assert twice["occurrences"]["09_compositional_test.md"] == 1
    assert [v["why"] for v in twice["violations"]] == ["outside its home"] * 3


def test_b1_caveats_map_reads():
    m = ROOT / "paper" / "v3" / "checks" / "caveats.yaml"
    if not m.exists():
        pytest.skip("B1's map not written yet")
    cvs, problems = vc.parse_caveats(m)
    assert not problems and len(cvs) >= 30
    sc = vc.scope_from_map(m)
    assert sc.main_files and sc.appendix_files


@NEED_POPPLER
def test_pages_fail_on_v2():
    heads = vc.main_text_headings(vc.load_parts(V2))
    assert heads == {"end_heading": "Appendices", "start_heading": "1 Introduction"}
    res = vc.run_pages(
        V2_PDF, heads["end_heading"], heads["start_heading"], 15, "page1"
    )
    assert res["status"] == "FAIL"
    assert abs(res["from_page1"] - 33.42) < 0.01  # P1/P2: 33.42
    assert abs(res["from_section1"] - 31.55) < 0.02  # P1: 31.55
    assert (
        vc.run_pages(V2_PDF, "Appendices", "1 Introduction", 15, "section1")["status"]
        == "FAIL"
    )


@NEED_POPPLER
def test_legibility_fails_on_v2():
    res = vc.run_legibility(
        V2_PDF,
        (V2 / "out" / "submission_v2.md").read_text(encoding="utf-8"),
        json.loads((V2 / "out" / "files.json").read_text(encoding="utf-8")),
        8,
        7,
    )
    assert res["status"] == "FAIL" and len(res["images"]) == 15 and res["failing"] == 15
    assert (
        max(r["label_pt_printed"] for r in res["images"]) < 4.5
    )  # P2 §1.3: 2.5-4.3 pt


# ----------------------------------------------------------------- positive fixture


def test_terms_pass_on_fixture():
    res = vc.terms_check(
        POS, POS / "checks" / "terms.txt", POS / "checks" / "registered.txt"
    )
    assert res["status"] == "PASS", res["hits"]
    assert len(res["exempt_registered"]) == 1 and len(res["glossed"]) == 1
    assert len(res["in_code_not_graded"]) == 1


def test_dates_pass_on_fixture():
    res = vc.dates_check(POS, POS / "checks" / "dates_allow.txt")
    assert res["status"] == "PASS", res["hits"]
    assert len(res["allowed"]) == 1


def test_caveats_pass_on_fixture():
    res = vc.caveats_check(POS, POS / "checks" / "caveats.yaml")
    assert res["status"] == "PASS", res["caveats"]
    assert res["caveats"][0]["occurrences"] == {"05_worked_example.md": 1}
    assert res["caveats"][1]["status"] == "PASS"  # label_required


def _mutated(tmp_path: Path, name: str, old: str, new: str) -> Path:
    root = tmp_path / "pos"
    shutil.copytree(POS, root)
    f = root / "sections" / name
    text = f.read_text(encoding="utf-8")
    assert old in text
    f.write_text(text.replace(old, new), encoding="utf-8")
    return root


def test_fixture_mutations_fail(tmp_path):
    # a second gloss of the same term is a hit
    r = _mutated(
        tmp_path / "a",
        "01_introduction.md",
        "</figcaption>",
        " Again labelled “GPU 1” on the figure.</figcaption>",
    )
    assert (
        vc.terms_check(r, r / "checks" / "terms.txt", r / "checks" / "registered.txt")[
            "status"
        ]
        == "FAIL"
    )
    # a gloss outside a caption is not a gloss
    r = _mutated(
        tmp_path / "b",
        "05_worked_example.md",
        "always combined.",
        "always combined, labelled “GPU 1” on the figure.",
    )
    assert (
        vc.terms_check(r, r / "checks" / "terms.txt", r / "checks" / "registered.txt")[
            "status"
        ]
        == "FAIL"
    )
    # a date outside the allow-list, written as words
    r = _mutated(
        tmp_path / "c",
        "05_worked_example.md",
        "always combined.",
        "always combined, as ruled on 2 August 2026.",
    )
    assert vc.dates_check(r, r / "checks" / "dates_allow.txt")["status"] == "FAIL"
    # a project year in date context
    r = _mutated(
        tmp_path / "d",
        "05_worked_example.md",
        "always combined.",
        "always combined, as found in early 2026.",
    )
    assert vc.dates_check(r, r / "checks" / "dates_allow.txt")["status"] == "FAIL"
    # the caveat restated outside its home, even beside a link to the home
    r = _mutated(
        tmp_path / "e",
        "01_introduction.md",
        "the two arms differ in how often each coupling appears",
        "JOINT sees each coupling twice as often as ISO-4",
    )
    res = vc.caveats_check(r, r / "checks" / "caveats.yaml")
    assert (
        res["status"] == "FAIL" and res["caveats"][0]["violations"][0]["links_to_home"]
    )
    # the same caveat twice in its home (max_home 1)
    r = _mutated(
        tmp_path / "g",
        "05_worked_example.md",
        "always combined.",
        "always combined. Again, JOINT sees each coupling twice as often as ISO-4.",
    )
    assert vc.caveats_check(r, r / "checks" / "caveats.yaml")["status"] == "FAIL"
    # a post hoc result without its label
    r = _mutated(
        tmp_path / "h",
        "05_worked_example.md",
        "always combined.",
        "always combined.\n\nThe interaction check found nothing.",
    )
    assert vc.caveats_check(r, r / "checks" / "caveats.yaml")["status"] == "FAIL"
    # the caveat missing from its home
    r = _mutated(
        tmp_path / "f",
        "05_worked_example.md",
        "JOINT sees each coupling twice as often as ISO-4",
        "JOINT is described elsewhere",
    )
    assert vc.caveats_check(r, r / "checks" / "caveats.yaml")["status"] == "FAIL"


def _pdf(path: Path, pages: list[list[tuple[float, str, float]]]) -> None:
    """A US Letter PDF; each page a list of (y from top in pt, text, font size)."""
    import matplotlib

    matplotlib.use("Agg")
    matplotlib.rcParams["pdf.fonttype"] = 42
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages

    with PdfPages(path) as pdf:
        for items in pages:
            fig = plt.figure(figsize=(8.5, 11))
            for y, text, size in items:
                fig.text(158 / 612, 1 - y / 792, text, fontsize=size, va="top")
            pdf.savefig(fig)
            plt.close(fig)


@NEED_POPPLER
def test_pages_pass_on_fixture(tmp_path):
    pdf = tmp_path / "fixture.pdf"
    toc = [
        (40, "Fixture title", 20),
        (120, "Contents", 9),
        (135, "1 Introduction", 9),
        (150, "Appendices", 9),
    ]
    pages = [toc, [(100, "1 Introduction", 14), (200, "Body text.", 10)]]
    pages += [[(300, "Body text.", 10)] for _ in range(11)]
    pages += [[(396, "Appendices", 14), (500, "Appendix A text.", 10)]]
    _pdf(pdf, pages)
    names = ["1 Introduction", "Appendices"]
    res = vc.run_pages(pdf, names[1], names[0], 15, "page1")
    assert res["status"] == "PASS" and res["pages_in_pdf"] == 14
    assert abs(res["from_page1"] - 13.5) < 0.02  # page 14, y 396 of 792
    assert abs(res["from_section1"] - (13.5 - (1 + 100 / 792))) < 0.02
    assert (
        res["end"]["page"] == 14 and res["start"]["page"] == 2
    )  # not the contents entries
    assert (
        vc.run_pages(pdf, names[1], names[0], 12, "page1")["status"] == "FAIL"
    )  # the ceiling binds


@NEED_POPPLER
def test_legibility_passes_on_fixture(tmp_path):
    from PIL import Image, ImageDraw

    png = tmp_path / "companion.png"
    im = Image.new("RGB", (780, 390), "white")  # drawn 5.2 in at 150 dpi
    ImageDraw.Draw(im).text((20, 20), "label", fill="black")
    im.save(png, dpi=(150, 150))
    pdf = tmp_path / "print.pdf"
    im.save(pdf, resolution=150)  # printed 5.2 in wide
    src = '{% include figure.html path="assets/img/submission/companion.png" class="img-fluid" %}'
    res = vc.run_legibility(
        pdf, src, {"assets/img/submission/companion.png": str(png)}, 8, 7
    )
    assert res["status"] == "PASS" and res["images"][0]["label_pt_printed"] == 8.0
    small = tmp_path / "small.pdf"
    im.resize((260, 130)).save(small, resolution=150)  # printed at a third
    assert (
        vc.run_legibility(
            small, src, {"assets/img/submission/companion.png": str(png)}, 8, 7
        )["status"]
        == "FAIL"
    )


def test_cli_runs():
    out = subprocess.run(
        [
            sys.executable,
            str(SRC / "v3_checks.py"),
            "dates",
            "--root",
            str(POS),
            "--allow",
            str(POS / "checks" / "dates_allow.txt"),
        ],
        capture_output=True,
        text=True,
    )
    assert out.returncode == 0 and "dates: PASS" in out.stdout
