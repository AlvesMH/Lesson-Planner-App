# File: app/vectorstore.py
"""Vector‑store helpers.

* 1️⃣ Each embed model gets its **own** Chroma directory so dimensions never clash.
* 2️⃣ If a directory already exists but dimensions still mismatch (rare corruptions),
     it is automatically rebuilt so the user doesn’t have to delete it manually.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from functools import lru_cache
from typing import Sequence, Set

from chromadb.errors import InvalidArgumentError
from langchain.docstore.document import Document
from langchain_chroma import Chroma
from langchain_ollama.embeddings import OllamaEmbeddings

from .config import settings

# ---------------------------------------------------------------------------
#  Embeddings (singleton)                                                    #
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _embedder() -> OllamaEmbeddings:  # noqa: D401
    """Return a shared OllamaEmbeddings client using the model from settings."""
    return OllamaEmbeddings(model=settings.OLLAMA_EMBED_MODEL,
                            base_url=settings.OLLAMA_BASE_URL)

# ---------------------------------------------------------------------------
#  Storage directory depends on embed‑model                                 #
# ---------------------------------------------------------------------------

def _dir_for_model() -> Path:
    safe = settings.OLLAMA_EMBED_MODEL.replace(":", "_").replace("/", "_")
    return Path(settings.CHROMA_DIR).with_suffix("") / safe

# ---------------------------------------------------------------------------
#  Vector‑store factory                                                     #
# ---------------------------------------------------------------------------

def _open_chroma(path: Path) -> Chroma:
    return Chroma(persist_directory=str(path), embedding_function=_embedder())

def get_vectorstore() -> Chroma:  # noqa: D401
    """Open a Chroma DB; rebuild if embedding dimension mismatch."""
    path = _dir_for_model()
    path.mkdir(parents=True, exist_ok=True)

    try:
        return _open_chroma(path)
    except InvalidArgumentError as exc:
        # dimension mismatch – wipe and recreate
        shutil.rmtree(path, ignore_errors=True)
        path.mkdir(parents=True, exist_ok=True)
        return _open_chroma(path)

# ---------------------------------------------------------------------------
#  Document ingestion                                                       #
# ---------------------------------------------------------------------------

def _existing_hashes(vs: Chroma) -> Set[str]:  # type: ignore[valid-type]
    try:
        meta = vs._collection.get(include=["metadatas"])  # type: ignore[attr-defined]
        return {m["sha256"] for m in meta.get("metadatas", []) if m and "sha256" in m}
    except Exception:
        return set()

def add_new_documents(vs: Chroma, docs: Sequence[Document]) -> None:  # type: ignore[valid-type]
    if not docs:
        return
    fresh = [d for d in docs if d.metadata.get("sha256") not in _existing_hashes(vs)]
    if fresh:
        vs.add_documents(fresh)  # auto‑persist in Chroma ≥0.0.15

        
