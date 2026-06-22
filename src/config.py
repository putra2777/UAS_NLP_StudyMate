from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""

    google_api_key: str
    google_model: str
    demo_mode: bool
    quality_threshold: int
    max_revisions: int
    langsmith_tracing: bool
    langsmith_project: str


def get_settings() -> Settings:
    threshold = int(os.getenv("QUALITY_THRESHOLD", "80"))
    max_revisions = int(os.getenv("MAX_REVISIONS", "1"))

    if not 0 <= threshold <= 100:
        raise ValueError("QUALITY_THRESHOLD harus berada pada rentang 0-100.")
    if max_revisions < 0:
        raise ValueError("MAX_REVISIONS tidak boleh negatif.")

    return Settings(
        google_api_key=os.getenv("GOOGLE_API_KEY", "").strip(),
        google_model=os.getenv("GOOGLE_MODEL", "gemini-2.5-flash").strip(),
        demo_mode=_as_bool(os.getenv("DEMO_MODE"), False),
        quality_threshold=threshold,
        max_revisions=max_revisions,
        langsmith_tracing=_as_bool(os.getenv("LANGSMITH_TRACING"), True),
        langsmith_project=os.getenv("LANGSMITH_PROJECT", "uas-nlp-studymate").strip(),
    )
