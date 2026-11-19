from src.chunker import chunk_text, build_chunks

SAMPLE = "word " * 1000  # 5000 characters


def test_no_empty_chunks():
    assert all(len(c) > 0 for c in chunk_text(SAMPLE, size=300, overlap=50))


def test_chunks_never_exceed_size():
    assert all(len(c) <= 300 for c in chunk_text(SAMPLE, size=300, overlap=50))


def test_neighbouring_chunks_overlap():
    chunks = chunk_text(SAMPLE, size=300, overlap=50)
    for a, b in zip(chunks, chunks[1:]):
        assert a[-50:] == b[:50]


def test_chunks_carry_metadata():
    pages = [{"doc": "demo", "page": 7, "text": SAMPLE}]
    chunks = build_chunks(pages, size=300, overlap=50)
    for c in chunks:
        assert c["doc"] == "demo"
        assert c["page"] == 7
        assert isinstance(c["chunk_id"], int)
    assert [c["chunk_id"] for c in chunks] == list(range(len(chunks)))

from src.chunker import chunk_sentences

SENTENCES = " ".join(f"This is sentence number {i} about mutual funds." for i in range(60))


def test_sentence_chunks_nonempty_and_within_size():
    chunks = chunk_sentences(SENTENCES, size=300, overlap=60)
    assert all(0 < len(c) <= 300 for c in chunks)


def test_sentence_chunks_start_and_end_on_sentence_boundaries():
    for c in chunk_sentences(SENTENCES, size=300, overlap=60):
        assert c.startswith("This is sentence")
        assert c.endswith("mutual funds.")


def test_no_sentence_is_lost():
    joined = " ".join(chunk_sentences(SENTENCES, size=300, overlap=60))
    for i in range(60):
        assert f"sentence number {i} about" in joined