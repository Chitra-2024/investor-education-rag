import numpy as np

from src.retriever import retrieve

CHUNKS = [{"chunk_id": i, "doc": "d", "page": 1, "text": f"t{i}"} for i in range(5)]
VECS = np.eye(5, dtype=np.float32)  # chunk i points along axis i


def test_returns_exactly_k():
    q = np.array([1, 0, 0, 0, 0], dtype=np.float32)
    assert len(retrieve(q, VECS, CHUNKS, k=3)) == 3


def test_sorted_by_descending_score():
    q = np.array([0.1, 0.9, 0.3, 0.0, 0.0], dtype=np.float32)
    scores = [r["score"] for r in retrieve(q, VECS, CHUNKS, k=4)]
    assert scores == sorted(scores, reverse=True)
    assert retrieve(q, VECS, CHUNKS, k=1)[0]["chunk_id"] == 1