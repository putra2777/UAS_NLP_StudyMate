from __future__ import annotations

from collections.abc import Callable

from langgraph.graph import END, START, StateGraph

from src.chains import StudyChains, build_chains
from src.config import Settings
from src.state import StudyState
from src.utils import parse_score, route_after_validation, validate_input


def make_nodes(chains: StudyChains) -> dict[str, Callable[[StudyState], StudyState]]:
    def analyze_material(state: StudyState) -> StudyState:
        result = chains.analysis.invoke(
            {
                "subject": state["subject"],
                "difficulty": state["difficulty"],
                "source_text": state["source_text"],
            },
            config={
                "run_name": "langchain_analyze_material",
                "tags": ["uas-nlp", "analysis", "langchain"],
            },
        )
        return {"analysis": result}

    def summarize_material(state: StudyState) -> StudyState:
        result = chains.summary.invoke(
            {
                "subject": state["subject"],
                "difficulty": state["difficulty"],
                "source_text": state["source_text"],
                "analysis": state["analysis"],
            },
            config={
                "run_name": "langchain_generate_summary",
                "tags": ["uas-nlp", "summary", "langchain"],
            },
        )
        return {"summary": result}

    def create_quiz(state: StudyState) -> StudyState:
        result = chains.quiz.invoke(
            {
                "subject": state["subject"],
                "difficulty": state["difficulty"],
                "source_text": state["source_text"],
                "summary": state["summary"],
            },
            config={
                "run_name": "langchain_generate_quiz",
                "tags": ["uas-nlp", "quiz", "langchain"],
            },
        )
        return {"quiz": result}

    def quality_review(state: StudyState) -> StudyState:
        result = chains.review.invoke(
            {
                "source_text": state["source_text"],
                "analysis": state["analysis"],
                "summary": state["summary"],
                "quiz": state["quiz"],
            },
            config={
                "run_name": "langchain_quality_review",
                "tags": ["uas-nlp", "quality", "langchain"],
            },
        )
        return {"review": result, "quality_score": parse_score(result)}

    def revise_output(state: StudyState) -> StudyState:
        revised_summary = chains.revise_summary.invoke(
            {
                "source_text": state["source_text"],
                "summary": state["summary"],
                "review": state["review"],
            },
            config={
                "run_name": "langchain_revise_summary",
                "tags": ["uas-nlp", "revision", "langchain"],
            },
        )
        revised_quiz = chains.revise_quiz.invoke(
            {
                "source_text": state["source_text"],
                "quiz": state["quiz"],
                "review": state["review"],
            },
            config={
                "run_name": "langchain_revise_quiz",
                "tags": ["uas-nlp", "revision", "langchain"],
            },
        )
        return {
            "summary": revised_summary,
            "quiz": revised_quiz,
            "revision_count": state.get("revision_count", 0) + 1,
        }

    def finalize(state: StudyState) -> StudyState:
        final_output = (
            f"{state.get('summary', '')}\n\n"
            f"# Kuis Pemahaman\n\n{state.get('quiz', '')}"
        )
        return {"final_output": final_output}

    def handle_error(state: StudyState) -> StudyState:
        message = state.get("error", "Terjadi kesalahan validasi input.")
        return {"final_output": f"## Proses dihentikan\n\n{message}"}

    return {
        "analyze_material": analyze_material,
        "summarize_material": summarize_material,
        "create_quiz": create_quiz,
        "quality_review": quality_review,
        "revise_output": revise_output,
        "finalize": finalize,
        "handle_error": handle_error,
    }


def build_workflow(settings: Settings):
    """Compile the LangGraph state machine used by the application."""
    chains = build_chains(settings.google_model)
    nodes = make_nodes(chains)

    builder = StateGraph(StudyState)
    builder.add_node("validate_input", validate_input)
    for name, node in nodes.items():
        builder.add_node(name, node)

    builder.add_edge(START, "validate_input")
    builder.add_conditional_edges(
        "validate_input",
        route_after_validation,
        {"valid": "analyze_material", "invalid": "handle_error"},
    )
    builder.add_edge("analyze_material", "summarize_material")
    builder.add_edge("summarize_material", "create_quiz")
    builder.add_edge("create_quiz", "quality_review")

    def route_after_review(state: StudyState) -> str:
        score = state.get("quality_score", 0)
        revisions = state.get("revision_count", 0)
        if score < settings.quality_threshold and revisions < settings.max_revisions:
            return "revise"
        return "finish"

    builder.add_conditional_edges(
        "quality_review",
        route_after_review,
        {"revise": "revise_output", "finish": "finalize"},
    )
    builder.add_edge("revise_output", "quality_review")
    builder.add_edge("handle_error", END)
    builder.add_edge("finalize", END)

    return builder.compile()


def workflow_mermaid() -> str:
    """Static Mermaid source used in documentation and the Streamlit UI."""
    return """flowchart TD
    A([START]) --> B[Validate Input]
    B -->|Valid| C[Analyze Material]
    B -->|Invalid| X[Handle Error]
    C --> D[Generate Summary]
    D --> E[Generate Quiz]
    E --> F[Quality Review]
    F -->|Score < Threshold| G[Revise Output]
    G --> F
    F -->|Score >= Threshold or max revision| H[Finalize]
    X --> I([END])
    H --> I
"""
