import sys

import numpy as np

from src.embedder import embed_texts, index_dir_for, load_index
from src.evaluate import load_gold, norm, phrases_of

qid, size = sys.argv[1], int(sys.argv[2])
row = load_gold().query("id == @qid").iloc[0]
vecs, chunks, _ = load_index(index_dir_for(size))

scores = vecs @ embed_texts([row["question"]])[0]   # score of EVERY chunk
order = np.argsort(scores)[::-1]                    # chunk indices, best first
rank_of = {int(i): r for r, i in enumerate(order, start=1)}

print(f"Q{qid}: {row['question']}")
for ph in phrases_of(row):
    holders = [c for c in chunks if ph in norm(c["text"])]
    print(f"\nPhrase: {ph!r}")
    if not holders:
        print("  NOT inside any single chunk -> cut by a chunk boundary")
    for c in holders:
        i = c["chunk_id"]
        print(f"  in chunk {i} (p.{c['page']}): rank {rank_of[i]} of {len(chunks)}, score {scores[i]:.3f}")

print("\nTop 3 retrieved:")
for i in order[:3]:
    c = chunks[int(i)]
    print(f"  score {scores[i]:.3f}  {c['doc']} p.{c['page']}: {c['text'][:120]}...")