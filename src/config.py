from pathlib import Path

# Folders
ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "data" / "docs"
INDEX_DIR = ROOT / "data" / "index"

# Chunking
CHUNK_SIZE = 800     # characters per chunk
CHUNK_OVERLAP = 100  # characters shared between neighbouring chunks

# Retrieval
TOP_K = 4
SCORE_THRESHOLD = 0.0  # placeholder; we'll tune this from data later

# Embedding model
EMBED_MODEL = "all-MiniLM-L6-v2"