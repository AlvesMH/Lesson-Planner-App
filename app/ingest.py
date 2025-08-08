# File: app/ingest.py

"""Document ingestion & preprocessing utility."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import List, Tuple

from langchain.docstore.document import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredFileLoader,
    UnstructuredWordDocumentLoader,
)

from langchain.text_splitter import RecursiveCharacterTextSplitter

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def _hash_file(path: Path) -> str:
    """Return SHA‑256 hex digest for a file."""
    sha256 = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(8192), b""):
            sha256.update(block)
    return sha256.hexdigest()


def _load_single(path: Path) -> List[Document]:
    """Gracefully load one file; raise informative errors."""
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return PyPDFLoader(str(path)).load()
    if suffix in {".docx", ".doc"}:
        return UnstructuredWordDocumentLoader(str(path)).load()
    return UnstructuredFileLoader(str(path)).load()


def load_and_chunk(file_paths: List[Path]) -> Tuple[List[Document], List[str]]:
    """Load files → chunk documents. Returns (docs, warnings)."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    docs: List[Document] = []
    warnings: List[str] = []

    for path in file_paths:
        file_hash = _hash_file(path)
        try:
            raw_docs = _load_single(path)
        except Exception as exc:  # noqa: BLE001
            warnings.append(
                f"❌ Could not parse {path.name} ({exc.__class__.__name__}). "
                "Try re‑saving the file as PDF or DOCX."
            )
            continue

        for d in raw_docs:
            d.metadata.update({"sha256": file_hash, "source_path": str(path)})
        docs.extend(splitter.split_documents(raw_docs))

    return docs, warnings