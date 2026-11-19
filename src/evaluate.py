import pandas as pd

from src import config
from src.embedder import embed_texts, index_dir_for, load_index
from src.retriever import retrieve

GOLD_PATH = config.ROOT / "data" / "gold_questions.csv"


def norm(s):
    """Lowercase and collapse whitespace so PDF line breaks don't matter."""
    return " ".join(str(s).lower().split())


def load_gold(path=GOLD_PATH):
    return pd.read_csv(path, encoding="utf-8", dtype=str).fillna("")


def phrases_of(row):
    return [norm(p) for p in row["evidence_phrase"].split("||")]


def hit_and_rr(phrases, ranked_chunks):
    """ranked_chunks is best-first. A hit needs EVERY phrase inside some chunk.
    Reciprocal rank = 1 / (rank at which the last phrase is first found)."""
    first_ranks = []
    for ph in phrases:
        rank = next((i for i, c in enumerate(ranked_chunks, start=1)
                     if ph in norm(c["text"])), None)
        if rank is None:
            return False, 0.0
        first_ranks.append(rank)
    return True, 1 / max(first_ranks)


def evaluate_retrieval(size, ks=(3, 5)):
    vecs, chunks, meta = load_index(index_dir_for(size))
    gold = load_gold()
    answerable = gold[~gold["type"].isin(["unanswerable", "advice"])]
    qvecs = embed_texts(answerable["question"].tolist())
    top = [retrieve(q, vecs, chunks, k=max(ks)) for q in qvecs]

    results = []
    for k in ks:
        hits, rrs = [], []
        for (_, row), ranked in zip(answerable.iterrows(), top):
            hit, rr = hit_and_rr(phrases_of(row), ranked[:k])  # keep only top k
            hits.append(hit)
            rrs.append(rr)
            if not hit and k == max(ks):
                print(f"  chunk={size} k={k} MISS  Q{row['id']} ({row['type']})")
        results.append({
            "chunk_size": size,
            "k": k,
            "n_chunks": len(chunks),
            "hit_rate": sum(hits) / len(hits),
            "mrr": sum(rrs) / len(rrs),
        })
    return results


if __name__ == "__main__":
    rows = []
    for size in (500, 800, 1200):
        rows += evaluate_retrieval(size)
    df = pd.DataFrame(rows)
    print()
    print(df.to_string(index=False, float_format=lambda x: f"{x:.2f}"))
    df.to_csv(config.ROOT / "results" / "retrieval_results.csv", index=False)