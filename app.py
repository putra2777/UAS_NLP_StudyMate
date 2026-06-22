from __future__ import annotations

import os
from pathlib import Path

import streamlit as st

from src.config import get_settings
from src.demo import run_demo_workflow
from src.graph import build_workflow, workflow_mermaid

ROOT = Path(__file__).resolve().parent
SAMPLE_PATH = ROOT / "data" / "sample_materi.txt"

st.set_page_config(
    page_title="NLP StudyMate",
    page_icon="🧠",
    layout="wide",
)

st.title("NLP StudyMate")
st.caption(
    "Asisten belajar adaptif berbasis LangChain, LangGraph, dan LangSmith"
)

settings = get_settings()

with st.sidebar:
    st.header("Konfigurasi")
    st.write(f"**Model:** `{settings.google_model}`")
    st.write(f"**Quality threshold:** `{settings.quality_threshold}`")
    st.write(f"**Maksimal revisi:** `{settings.max_revisions}`")
    st.divider()
    st.subheader("Status")
    if settings.demo_mode:
        st.warning("DEMO_MODE aktif. Hasil tidak berasal dari LLM.")
    elif settings.google_api_key:
        st.success("Google API key terdeteksi.")
    else:
        st.error("Google API key belum diatur.")

    langsmith_key_exists = bool(os.getenv("LANGSMITH_API_KEY", "").strip())
    if settings.langsmith_tracing and langsmith_key_exists:
        st.success(f"LangSmith aktif: `{settings.langsmith_project}`")
    else:
        st.info("LangSmith belum aktif atau API key belum tersedia.")

if "source_text" not in st.session_state:
    st.session_state.source_text = SAMPLE_PATH.read_text(encoding="utf-8")

input_tab, result_tab, workflow_tab = st.tabs(
    ["1. Input Materi", "2. Hasil", "3. Workflow & Library"]
)

with input_tab:
    col1, col2 = st.columns([2, 1])
    with col1:
        subject = st.text_input(
            "Mata kuliah atau topik",
            value="Natural Language Processing",
        )
    with col2:
        difficulty = st.selectbox(
            "Tingkat kesulitan",
            ["Dasar", "Menengah", "Lanjut"],
            index=1,
        )

    source_text = st.text_area(
        "Masukkan materi yang akan dianalisis",
        value=st.session_state.source_text,
        height=340,
        help="Minimal 120 karakter.",
    )

    col_run, col_reset = st.columns([1, 1])
    with col_run:
        run_clicked = st.button("Jalankan Workflow", type="primary", use_container_width=True)
    with col_reset:
        if st.button("Muat Ulang Contoh", use_container_width=True):
            st.session_state.source_text = SAMPLE_PATH.read_text(encoding="utf-8")
            st.rerun()

    if run_clicked:
        if not settings.demo_mode and not settings.google_api_key:
            st.error(
                "GOOGLE_API_KEY belum diatur. Salin `.env.example` menjadi `.env`, "
                "isi API key, lalu restart aplikasi."
            )
        else:
            initial_state = {
                "subject": subject.strip() or "Topik tanpa judul",
                "difficulty": difficulty,
                "source_text": source_text.strip(),
                "revision_count": 0,
            }

            with st.status("Memproses materi...", expanded=True) as status:
                try:
                    if settings.demo_mode:
                        st.write("Menjalankan mode demo...")
                        result = run_demo_workflow(initial_state)
                    else:
                        st.write("Membangun LangGraph workflow...")
                        workflow = build_workflow(settings)
                        st.write("Menjalankan node analisis, ringkasan, kuis, dan review...")
                        result = workflow.invoke(
                            initial_state,
                            config={
                                "run_name": "uas_nlp_studymate_workflow",
                                "tags": ["uas-nlp", "langgraph", "studymate"],
                                "metadata": {
                                    "subject": initial_state["subject"],
                                    "difficulty": initial_state["difficulty"],
                                },
                            },
                        )
                    st.session_state.result = result
                    status.update(label="Workflow selesai.", state="complete")
                except Exception as exc:  # UI-level safety net
                    status.update(label="Workflow gagal.", state="error")
                    st.exception(exc)

with result_tab:
    result = st.session_state.get("result")
    if not result:
        st.info("Jalankan workflow pada tab Input Materi untuk melihat hasil.")
    else:
        metric1, metric2, metric3 = st.columns(3)
        metric1.metric("Quality Score", result.get("quality_score", 0))
        metric2.metric("Jumlah Revisi", result.get("revision_count", 0))
        metric3.metric("Status", "Selesai" if not result.get("error") else "Input tidak valid")

        if result.get("error"):
            st.error(result["error"])

        st.subheader("Analisis Materi")
        st.markdown(result.get("analysis", "Tidak tersedia."))

        st.subheader("Ringkasan")
        st.markdown(result.get("summary", "Tidak tersedia."))

        st.subheader("Kuis")
        st.markdown(result.get("quiz", "Tidak tersedia."))

        with st.expander("Lihat Quality Review"):
            st.code(result.get("review", "Tidak tersedia."), language="text")

        st.download_button(
            "Unduh Hasil Markdown",
            data=result.get("final_output", ""),
            file_name="hasil_studymate.md",
            mime="text/markdown",
        )

with workflow_tab:
    st.subheader("Pembagian Peran Library")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            "### LangChain\n"
            "Menyusun `ChatPromptTemplate`, memanggil model Gemini, dan memproses "
            "output melalui `StrOutputParser`."
        )
    with c2:
        st.markdown(
            "### LangGraph\n"
            "Mengelola state, node, edge, conditional routing, dan loop revisi "
            "berdasarkan quality score."
        )
    with c3:
        st.markdown(
            "### LangSmith\n"
            "Mencatat trace, durasi, input-output, metadata, dan urutan eksekusi "
            "untuk debugging serta observabilitas."
        )

    st.subheader("Alur LangGraph")
    st.code(workflow_mermaid(), language="mermaid")
    st.caption(
        "Salin kode Mermaid di atas ke Mermaid Live Editor atau tampilkan file "
        "`docs/architecture.png` ketika menjelaskan video."
    )
