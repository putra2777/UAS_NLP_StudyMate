from __future__ import annotations

from typing import TypedDict


class StudyState(TypedDict, total=False):
    """State shared by all nodes in the LangGraph workflow."""

    subject: str
    difficulty: str
    source_text: str
    analysis: str
    summary: str
    quiz: str
    review: str
    quality_score: int
    revision_count: int
    final_output: str
    error: str
