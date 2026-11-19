import numpy as np


def retrieve(query_vec, chunk_vecs, chunks, k=4):
    """Return the k most similar chunks, best first, each with a 'score' field."""
    scores = chunk_vecs @ query_vec            # one cosine score per chunk
    top = np.argsort(scores)[::-1][:k]         # indices of the k highest scores
    return [dict(chunks[i], score=float(scores[i])) for i in top]