import re
from collections import Counter
from pathlib import Path

from pypdf import PdfReader

from src.config import DOCS_DIR


def load_pdf(path):
    """Read one PDF page by page. Returns a list of {doc, page, text}."""
    reader = PdfReader(path)
    pages = []
    for i, page in enumerate(reader.pages, start=1):  # start=1: humans count pages from 1
        text = page.extract_text() or ""
        pages.append({"doc": Path(path).stem, "page": i, "text": text})
    return pages


def _normalise_line(line):
    # Replace digits with '#' so "Page 3" and "Page 4" look identical
    return re.sub(r"\d+", "#", line.strip().lower())


def find_repeated_lines(pages, threshold=0.4):
    """Find lines that appear on many pages (headers/footers/page numbers)."""
    counts = Counter()
    for p in pages:
        lines = {_normalise_line(l) for l in p["text"].splitlines() if l.strip()}
        counts.update(lines)
    n_pages = len(pages)
    return {line for line, c in counts.items() if c / n_pages >= threshold}


def clean_page(text, repeated_lines):
    # 0. Turn glyph names like "/uni20B9.INDIAN_RUPEE_SIGN" back into the real character
    text = re.sub(r"/uni([0-9A-Fa-f]{4})\.[A-Z_]+",
                  lambda m: chr(int(m.group(1), 16)), text)
    # 1. Drop header/footer lines
    kept = [l for l in text.splitlines()
            if l.strip() and _normalise_line(l) not in repeated_lines]
    text = "\n".join(kept)
    # 2. Rejoin words split by a hyphen at the end of a line
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    # 3. Collapse all whitespace into single spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_all(docs_dir=DOCS_DIR, min_chars=50):
    """Load, clean and return all pages from every PDF in docs_dir."""
    all_pages = []
    for pdf_path in sorted(Path(docs_dir).glob("*.pdf")):
        pages = load_pdf(pdf_path)
        repeated = find_repeated_lines(pages)
        for p in pages:
            p["text"] = clean_page(p["text"], repeated)
            if len(p["text"]) >= min_chars:  # drop near-empty pages
                all_pages.append(p)
    return all_pages


if __name__ == "__main__":
    pages = load_all()
    print(f"Loaded {len(pages)} pages")
    for doc in sorted({p["doc"] for p in pages}):
        n = sum(1 for p in pages if p["doc"] == doc)
        print(f"  {doc}: {n} pages")
    # Print a sample so you can inspect by eye
    sample = pages[len(pages) // 2]
    print(f"\n--- {sample['doc']} p.{sample['page']} ---")
    print(sample["text"][:1000])