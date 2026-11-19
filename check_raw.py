import sys
from pypdf import PdfReader
from src.config import DOCS_DIR

name, page_no = sys.argv[1], int(sys.argv[2])
raw = PdfReader(DOCS_DIR / f"{name}.pdf").pages[page_no - 1].extract_text()
i = raw.find("investor should refer")
print(repr(raw[i:i + 400]))