from __future__ import annotations

from pathlib import Path

from src.config import get_settings
from src.demo import run_demo_workflow
from src.graph import build_workflow


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    material = (root / "data" / "sample_materi.txt").read_text(encoding="utf-8")
    settings = get_settings()
    initial_state = {
        "subject": "Natural Language Processing",
        "difficulty": "Menengah",
        "source_text": material,
        "revision_count": 0,
    }

    if settings.demo_mode:
        result = run_demo_workflow(initial_state)
    else:
        if not settings.google_api_key:
            raise RuntimeError(
                "GOOGLE_API_KEY belum diatur. Isi file .env atau aktifkan DEMO_MODE=true."
            )
        graph = build_workflow(settings)
        result = graph.invoke(
            initial_state,
            config={"run_name": "uas_nlp_cli_demo", "tags": ["uas-nlp", "cli"]},
        )

    print("\n=== QUALITY SCORE ===")
    print(result.get("quality_score", 0))
    print("\n=== FINAL OUTPUT ===")
    print(result.get("final_output", ""))


if __name__ == "__main__":
    main()
