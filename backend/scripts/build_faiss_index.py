"""
Build a FAISS index over both KB markdown and PDF chunks.
Usage:
  python scripts/build_faiss_index.py
"""
from pathlib import Path
import json, faiss, numpy as np
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).parents[1]
KB_DIR = ROOT / "app" / "kb"
CHUNK_DIR = ROOT / "app" / "kb_chunks"
INDEX_PATH = ROOT / "app" / "vector.index"
META_PATH = ROOT / "app" / "vector_meta.jsonl"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def read_docs():
    docs = []
    if KB_DIR.exists():
        for p in KB_DIR.glob("**/*.md"):
            try:
                docs.append({"id": str(p.relative_to(ROOT)), "content": p.read_text(encoding="utf-8"), "source": "kb", "url": None})
            except: pass
    if CHUNK_DIR.exists():
        for p in sorted(CHUNK_DIR.glob("*.txt")):
            try:
                docs.append({"id": str(p.relative_to(ROOT)), "content": p.read_text(encoding="utf-8"), "source": "gale_pdf", "url": None})
            except: pass
    return docs

def main():
    docs = read_docs()
    if not docs:
        print("[WARN] No docs found in app/kb or app/kb_chunks"); return
    model = SentenceTransformer(MODEL_NAME)
    texts = [d["content"][:4000] for d in docs]
    embs = model.encode(texts, batch_size=64, show_progress_bar=True, normalize_embeddings=True)
    embs = np.asarray(embs).astype("float32")

    index = faiss.IndexFlatIP(embs.shape[1])
    index.add(embs)

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_PATH))
    with open(META_PATH, "w", encoding="utf-8") as f:
        for d in docs:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    print(f"[OK] Saved {len(docs)} docs to {INDEX_PATH} and {META_PATH}")

if __name__ == "__main__":
    main()
