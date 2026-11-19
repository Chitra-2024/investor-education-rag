from src.evaluate import hit_and_rr

CHUNKS = [{"text": "alpha beta"}, {"text": "gamma  DELTA"}, {"text": "epsilon"}]


def test_hit_at_rank_two_scores_half():
    assert hit_and_rr(["gamma delta"], CHUNKS) == (True, 0.5)


def test_miss_scores_zero():
    assert hit_and_rr(["not present"], CHUNKS) == (False, 0.0)


def test_multi_phrase_needs_all_and_uses_last_rank():
    assert hit_and_rr(["alpha", "epsilon"], CHUNKS) == (True, 1 / 3)
    assert hit_and_rr(["alpha", "missing"], CHUNKS) == (False, 0.0)