import pandas as pd
from src.loader import load_all


def norm(s):
    return " ".join(str(s).lower().split())


pages = {(p["doc"], p["page"]): norm(p["text"]) for p in load_all()}
df = pd.read_csv("data/gold_questions.csv", encoding="utf-8", dtype=str).fillna("")

print(df["type"].value_counts(), "\n")

problems = 0
for _, r in df.iterrows():
    if r["type"] in ("unanswerable", "advice"):
        continue
    phrases = r["evidence_phrase"].split("||")
    expected = [int(x) for x in r["page"].split("|")]
    for raw, pg in zip(phrases, expected):
        ph = norm(raw)
        found = [p for (d, p), t in pages.items() if d == r["doc"] and ph in t]
        if not found:
            print(f"Q{r['id']}: NOT FOUND in {r['doc']}: {raw.strip()!r}")
            problems += 1
        elif pg not in found:
            print(f"Q{r['id']}: phrase is on page(s) {found}, but CSV says {pg}")
            problems += 1
        elif len(found) > 1:
            print(f"Q{r['id']}: WARNING phrase appears on several pages {found}; make it more specific")

print(f"\n{len(df)} questions, {problems} problem(s)")