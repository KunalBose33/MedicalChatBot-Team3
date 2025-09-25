from __future__ import annotations
from typing import List, Dict
from pathlib import Path
import json, faiss, numpy as np
from sentence_transformers import SentenceTransformer
from app.config.settings import settings

class FaissRetriever:
    def __init__(self,
                 index_path: str | Path = None,
                 meta_path: str | Path = None,
                 model_name: str = None):
        self.index_path = Path(index_path or settings.FAISS_INDEX_PATH)
        self.meta_path = Path(meta_path or settings.FAISS_META_PATH)
        self.model_name = model_name or settings.EMBED_MODEL
        if not self.index_path.exists() or not self.meta_path.exists():
            raise RuntimeError("FAISS index/meta not found. Run scripts/build_faiss_index.py first.")
        self.index = faiss.read_index(str(self.index_path))
        self.model = SentenceTransformer(self.model_name)
        self.meta: List[Dict] = []
        with open(self.meta_path, "r", encoding="utf-8") as f:
            for line in f:
                self.meta.append(json.loads(line))

    def retrieve(self, query: str, k: int = 5) -> List[Dict]:
        q = self.model.encode([query], normalize_embeddings=True)
        q = np.asarray(q).astype("float32")
        scores, idxs = self.index.search(q, k)
        out = []
        for i, score in zip(idxs[0], scores[0]):
            if i == -1: continue
            d = self.meta[i].copy()
            d["score"] = float(score)
            out.append(d)
        return out
