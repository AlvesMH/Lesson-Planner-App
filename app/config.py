# File: app/config.py
"""
Global settings – compatible with Pydantic v1/v2.
All configuration can be overridden via environment variables.
"""

from __future__ import annotations

import os
from functools import lru_cache

# ------------------------------------------------------------
#  Pydantic compatibility layer
# ------------------------------------------------------------
try:  # Pydantic v2
    from pydantic_settings import BaseSettings
    from pydantic import Field
except ModuleNotFoundError:  # Pydantic v1
    from pydantic import BaseSettings, Field  # type: ignore
# ------------------------------------------------------------


class Settings(BaseSettings):
    """Central application settings (auto-read from env)."""

    # ——— URLs & models ———
    OLLAMA_BASE_URL: str = Field(
        default="http://localhost:11434",
        description="Base URL for the local Ollama server",
    )
    LLM_MODEL: str = Field(
        default="gpt-oss:20b",
        description="Chat/LLM model tag served by Ollama",
    )
    OLLAMA_EMBED_MODEL: str = Field(
        default="nomic-embed-text:v1.5",
        description="Embedding model tag served by Ollama",
    )

    # ——— Vector DB ———
    CHROMA_DIR: str = Field(
        default="chroma_lessons",
        description="Persistent directory for Chroma vector-store",
    )

    class Config:
        env_file = ".env"  # optional: pick up values from a local .env file
        case_sensitive = False


# cache the instance so every import gets the same object
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


# convenience alias – preserves the old ``from .config import settings`` import
settings = get_settings()


