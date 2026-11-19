import json

import numpy as np
from sentence_transformers import SentenceTransformer

from src.config import EMBED_MODEL, INDEX_DIR

_model = None  # loaded once, reused afterwards


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


def embed_texts(texts):
    """Return an array of shape (len(texts), 384); every row has length 1."""
    return get_model().encode(texts, normalize_embeddings=True, show_progress_bar=False)


def index_dir_for(chunk_size):
    """One folder per chunk size, e.g. data/index/c800."""
    return INDEX_DIR / f"c{chunk_size}"


def build_index(chunks, index_dir, chunk_size, overlap):
    index_dir.mkdir(parents=True, exist_ok=True)
    vecs = embed_texts([c["text"] for c in chunks])
    np.save(index_dir / "embeddings.npy", vecs)
    with open(index_dir / "chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False)
    meta = {"chunk_size": chunk_size, "overlap": overlap,
            "model": EMBED_MODEL, "n_chunks": len(chunks)}
    with open(index_dir / "index_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print(f"Saved {len(chunks)} chunks to {index_dir}")


def load_index(index_dir):
    vecs = np.load(index_dir / "embeddings.npy")
    with open(index_dir / "chunks.json", encoding="utf-8") as f:
        chunks = json.load(f)
    with open(index_dir / "index_meta.json", encoding="utf-8") as f:
        meta = json.load(f)
    return vecs, chunks, meta