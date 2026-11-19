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