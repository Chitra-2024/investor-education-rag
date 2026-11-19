from src.config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split one string into overlapping pieces of at most `size` characters."""
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    chunks, start = [], 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap  # step back so neighbouring chunks overlap
    return chunks


def build_chunks(pages, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Turn a list of pages into chunks, each tagged with doc, page and chunk_id."""
    all_chunks = []
    for p in pages:
        for piece in chunk_text(p["text"], size, overlap):
            all_chunks.append({
                "chunk_id": len(all_chunks),  # 0, 1, 2, ... across everything
                "doc": p["doc"],
                "page": p["page"],
                "text": piece,
            })
    return all_chunks


if __name__ == "__main__":
    from src.loader import load_all

    chunks = build_chunks(load_all())
    print(f"{len(chunks)} chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    print(chunks[100])