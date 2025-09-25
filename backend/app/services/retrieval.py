from __future__ import annotations
from pathlib import Path
import math
from app.config.settings import settings

class InMemoryRetriever:
    def __init__(self, kb_dir: str | Path = None, chunk_dir: str | Path = None):
        base = Path(__file__).parents[1]
        self.kb_dir = Path(kb_dir or base / "kb")
        self.chunk_dir = Path(chunk_dir or base / "kb_chunks")
        self.docs = []
        if self.kb_dir.exists():
            for p in self.kb_dir.glob("**/*.md"):
                try:
                    self.docs.append({"id": p.name, "content": p.read_text(encoding="utf-8"), "source": "kb", "url": None})
                except: 
                    pass
        if self.chunk_dir.exists():
            for p in sorted(self.chunk_dir.glob("*.txt")):
                try:
                    self.docs.append({"id": p.name, "content": p.read_text(encoding="utf-8"), "source": "gale_pdf", "url": None})
                except: 
                    pass

    def _score(self, query: str, content: str) -> float:
        tokens = [t for t in query.lower().split() if len(t) > 2]
        if not tokens: return 0.0
        cl = content.lower()
        score = sum(cl.count(t) for t in tokens)
        return score / math.sqrt(len(content) + 1)

    def retrieve(self, query: str, k: int = 5):
        ranked = sorted(self.docs, key=lambda d: self._score(query, d["content"]), reverse=True)
        return ranked[:k]

def get_retriever():
    if getattr(settings, "USE_FAISS", False):
        from .retrieval_faiss import FaissRetriever
        return FaissRetriever(index_path=settings.FAISS_INDEX_PATH,
                              meta_path=settings.FAISS_META_PATH,
                              model_name=settings.EMBED_MODEL)
    return InMemoryRetriever()
