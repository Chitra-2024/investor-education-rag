from src.config import CHUNK_SIZE, CHUNK_OVERLAP
import re

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

def split_sentences(text):
    """Split after . ? ! when a new sentence, bullet or number follows."""
    return re.split(r"(?<=[.!?])\s+(?=[A-Z0-9●•(\[“\"])", text)


def chunk_sentences(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Pack whole sentences into chunks of at most `size` characters.
    Each new chunk starts with the last sentence(s) of the previous one
    (up to `overlap` characters), so ideas that straddle a boundary survive."""
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    chunks, current, length = [], [], 0
    for s in split_sentences(text):
        if len(s) > size:  # one huge sentence: fall back to character chunks
            if current:
                chunks.append(" ".join(current))
                current, length = [], 0
            chunks.extend(chunk_text(s, size, overlap))
            continue
        if current and length + len(s) + 1 > size:
            chunks.append(" ".join(current))
            carry, total = [], 0
            for prev in reversed(current):  # carry trailing sentences as overlap
                if total + len(prev) + 1 > overlap:
                    break
                carry.insert(0, prev)
                total += len(prev) + 1
            if total + len(s) + 1 > size:
                carry, total = [], 0
            current, length = carry, total
        current.append(s)
        length += len(s) + 1
    if current:
        chunks.append(" ".join(current))
    return chunks


def build_chunks(pages, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP, mode="char"):
    """Turn pages into chunks tagged with doc, page and chunk_id."""
    splitter = chunk_sentences if mode == "sentence" else chunk_text
    all_chunks = []
    for p in pages:
        for piece in splitter(p["text"], size, overlap):
            all_chunks.append({
                "chunk_id": len(all_chunks),
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