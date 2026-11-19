import argparse

from src import config
from src.chunker import build_chunks
from src.embedder import build_index, embed_texts, index_dir_for, load_index
from src.loader import load_all
from src.retriever import retrieve


def cmd_build(args):
    chunks = build_chunks(load_all(), args.size, args.overlap)
    build_index(chunks, index_dir_for(args.size), args.size, args.overlap)


def cmd_ask(args):
    vecs, chunks, meta = load_index(index_dir_for(args.size))
    query_vec = embed_texts([args.question])[0]
    for rank, r in enumerate(retrieve(query_vec, vecs, chunks, k=args.k), start=1):
        print(f"\n[{rank}] score={r['score']:.3f}  {r['doc']}  p.{r['page']}  (chunk {r['chunk_id']})")
        print(r["text"])


def main():
    parser = argparse.ArgumentParser(description="Investor Education RAG")
    sub = parser.add_subparsers(dest="command", required=True)

    b = sub.add_parser("build", help="build the index")
    b.add_argument("--size", type=int, default=config.CHUNK_SIZE)
    b.add_argument("--overlap", type=int, default=config.CHUNK_OVERLAP)
    b.set_defaults(func=cmd_build)

    a = sub.add_parser("ask", help="ask a question")
    a.add_argument("question")
    a.add_argument("--size", type=int, default=config.CHUNK_SIZE)
    a.add_argument("--k", type=int, default=config.TOP_K)
    a.set_defaults(func=cmd_ask)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()