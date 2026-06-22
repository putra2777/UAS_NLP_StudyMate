from __future__ import annotations

import re

from src.state import StudyState


def parse_score(review_text: str) -> int:
    """Extract SCORE value safely from model output and clamp it to 0-100."""
    match = re.search(r"SCORE\s*:\s*(\d{1,3})", review_text, flags=re.IGNORECASE)
    if not match:
        return 0
    return max(0, min(100, int(match.group(1))))


def validate_input(state: StudyState) -> StudyState:
    """Validate the source material before the LLM workflow is executed."""
    text = state.get("source_text", "").strip()
    if len(text) < 120:
        return {
            "error": (
                "Materi terlalu pendek. Masukkan minimal 120 karakter agar analisis "
                "dan evaluasi memiliki konteks yang cukup."
            ),
            "revision_count": 0,
        }
    return {"error": "", "revision_count": state.get("revision_count", 0)}


def route_after_validation(state: StudyState) -> str:
    """Route workflow based on input validation result."""
    return "invalid" if state.get("error") else "valid"
