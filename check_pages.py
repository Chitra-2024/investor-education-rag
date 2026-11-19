import sys
from src.loader import load_all

pages = load_all()
doc_prefix = sys.argv[1]       # e.g. amfi
page_no = int(sys.argv[2])     # e.g. 8

for p in pages:
    if p["doc"].startswith(doc_prefix) and p["page"] == page_no:
        print(f"--- {p['doc']} p.{p['page']} ({len(p['text'])} chars) ---")
        print(p["text"])