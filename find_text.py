import sys
from src.loader import load_all


def norm(s):
    return " ".join(s.lower().split())


query = norm(" ".join(sys.argv[1:]))
for p in load_all():
    text = norm(p["text"])
    i = text.find(query)
    if i != -1:
        print(f"{p['doc']}  p.{p['page']}  ...{text[max(0, i - 60): i + len(query) + 60]}...")