"""
fetch_sources.py -- rebuild sources/ from the manifest.

The papers, their text extractions and the saved web pages are not committed (they are other
people's work). This script re-downloads them so a fresh clone can follow every citation in
INDEX.md.

    python tools/fetch_sources.py            # everything missing
    python tools/fetch_sources.py --force    # re-download all

Papers come from sources/papers/MANIFEST.tsv (columns: arxiv_id, file_stem, ...). PDFs that are not on
arXiv are listed in PDFS below (text extracted with PyMuPDF when it is installed: `pip install pymupdf`).
Web pages are listed below. Be polite to arXiv: one request every 1.5 s.
"""
import datetime
import html
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "sources" / "papers"
TEXT = ROOT / "sources" / "papers-text"
WEB = ROOT / "sources" / "web"
UA = {"User-Agent": "Mozilla/5.0 (warp-shell-check source archive)"}

WEB_PAGES = [
    ("https://applied-physics.gitbook.io/warp-factory", "warpfactory_docs_overview"),
    ("https://applied-physics.gitbook.io/warp-factory/overview/installing-warp-factory", "warpfactory_docs_installing"),
    ("https://applied-physics.gitbook.io/warp-factory/examples/analysis/a1-energy-conditions", "warpfactory_docs_a1_energy_conditions"),
    ("https://github.com/NerdsWithAttitudes/WarpFactory", "github_warpfactory_readme"),
    ("https://github.com/NerdsWithAttitudes/WarpFactory/issues/1", "github_warpfactory_issue1_python_version"),
    ("https://github.com/anindex/warpax", "github_warpax_readme"),
    ("https://zenodo.org/records/22728088", "zenodo_warpax_record"),
    ("https://github.com/matlab-actions/setup-matlab", "github_matlab_actions_setup_matlab_licensing"),
    ("https://appliedphysics.org/warp-grants/", "appliedphysics_warp_grants"),
    ("https://astro.theoj.org/article/121868-what-no-one-has-seen-before-gravitational-waveforms-from-warp-drive-collapse", "oja_clough_collapse_published"),
]

# PDFs that are not on arXiv: (url, file stem). Saved to sources/papers/ like the arXiv ones; the text
# extraction (PyMuPDF, one "=== page N ===" marker per page) goes to sources/papers-text/.
PDFS = [
    ("https://ntrs.nasa.gov/api/citations/20110015936/downloads/20110015936.pdf",
     "2011_white_warp_field_mechanics_101_ntrs_20110015936"),
    ("https://ntrs.nasa.gov/api/citations/20130011213/downloads/20130011213.pdf",
     "2013_white_warp_field_mechanics_102_energy_optimization_ntrs_20130011213"),
]


def get(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "replace")


def strip_tags(raw):
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<style.*?</style>", " ", raw, flags=re.S)
    raw = re.sub(r"<annotation.*?</annotation>", " ", raw, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    t = re.sub(r"[ \t\r\f\v]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t.strip()


def main(force=False):
    today = datetime.date.today().isoformat()
    for d in (PAPERS, TEXT, WEB):
        d.mkdir(parents=True, exist_ok=True)
    rows = [ln.split("\t") for ln in (PAPERS / "MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:] if ln.strip()]
    for row in rows:
        aid, stem = row[0], row[1]
        safe = aid.replace("/", "_")
        pdf_path = PAPERS / f"{stem}_{safe}.pdf"
        txt_path = TEXT / f"{stem}_{safe}.txt"
        if pdf_path.exists() and not force:
            print(f"  have   {pdf_path.name}")
        else:
            pdf = get(f"https://arxiv.org/pdf/{aid}", binary=True)
            if pdf[:5] == b"%PDF-":
                pdf_path.write_bytes(pdf)
                print(f"  pdf    {pdf_path.name} ({len(pdf) // 1024} KB)")
            else:
                print(f"  FAIL   {aid}: not a PDF")
            time.sleep(1.5)
        if not txt_path.exists() or force:
            try:
                t = strip_tags(get(f"https://arxiv.org/html/{aid}"))
                if len(t) > 20000:
                    txt_path.write_text(f"SOURCE: https://arxiv.org/html/{aid}\nRETRIEVED: {today}\n\n{t}", encoding="utf-8")
                    print(f"  text   {txt_path.name}")
            except Exception as e:  # old papers have no HTML version
                print(f"  nohtml {aid} ({type(e).__name__})")
            time.sleep(1.5)
            if not txt_path.exists() and pdf_path.exists():   # fall back to the PDF's text, as for PDFS below
                try:
                    import pymupdf
                except ImportError:
                    pymupdf = None
                if pymupdf is not None:
                    doc = pymupdf.open(pdf_path)
                    pages = [f"=== page {i + 1} ===\n{page.get_text()}" for i, page in enumerate(doc)]
                    txt_path.write_text(f"SOURCE: https://arxiv.org/pdf/{aid} (no HTML version; text by PyMuPDF)\nRETRIEVED: {today}\n\n"
                                        + "\n".join(pages), encoding="utf-8", newline="\n")
                    print(f"  text   {txt_path.name} (PyMuPDF, {doc.page_count} pages)")
    for url, stem in PDFS:
        pdf_path = PAPERS / f"{stem}.pdf"
        txt_path = TEXT / f"{stem}.txt"
        if pdf_path.exists() and not force:
            print(f"  have   {pdf_path.name}")
        else:
            pdf = get(url, binary=True)
            if pdf[:5] == b"%PDF-":
                pdf_path.write_bytes(pdf)
                print(f"  pdf    {pdf_path.name} ({len(pdf) // 1024} KB)")
            else:
                print(f"  FAIL   {stem}: not a PDF")
            time.sleep(1.5)
        if pdf_path.exists() and (not txt_path.exists() or force):
            try:
                import pymupdf
            except ImportError:
                print(f"  notext {stem}: PyMuPDF not installed (pip install pymupdf)")
                continue
            doc = pymupdf.open(pdf_path)
            pages = [f"=== page {i + 1} ===\n{page.get_text()}" for i, page in enumerate(doc)]
            txt_path.write_text(f"SOURCE: {url}\nRETRIEVED: {today}\n\n" + "\n".join(pages), encoding="utf-8", newline="\n")
            print(f"  text   {txt_path.name} (PyMuPDF, {doc.page_count} pages)")
    for url, name in WEB_PAGES:
        path = WEB / f"{name}.md"
        if path.exists() and not force:
            continue
        try:
            raw = get(url)
            m = re.search(r"<title>(.*?)</title>", raw, re.S)
            title = html.unescape(m.group(1)).strip() if m else name
            path.write_text(f"# {title}\n\nSource: {url}\nRetrieved: {today}\nNote: tag-stripped page text.\n\n---\n\n{strip_tags(raw)}", encoding="utf-8")
            print(f"  web    {name}")
        except Exception as e:
            print(f"  FAIL   {name}: {type(e).__name__}: {e}")
        time.sleep(1.0)


if __name__ == "__main__":
    main(force="--force" in sys.argv)
