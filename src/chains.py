from __future__ import annotations

from dataclasses import dataclass

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


@dataclass
class StudyChains:
    analysis: object
    summary: object
    quiz: object
    review: object
    revise_summary: object
    revise_quiz: object


def build_llm(model_name: str) -> ChatGoogleGenerativeAI:
    """Create the LangChain model wrapper used by every chain."""
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0.2,
        max_retries=2,
    )


def build_chains(model_name: str) -> StudyChains:
    """Build composable LangChain prompt-model-parser pipelines."""
    llm = build_llm(model_name)
    parser = StrOutputParser()

    analysis_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Anda adalah analis materi kuliah. Analisis isi secara objektif, "
                "gunakan bahasa Indonesia yang jelas, dan jangan menambahkan fakta "
                "yang tidak tersedia pada materi.",
            ),
            (
                "human",
                "Mata kuliah/topik: {subject}\n"
                "Tingkat kesulitan: {difficulty}\n\n"
                "Materi:\n{source_text}\n\n"
                "Buat analisis dalam format berikut:\n"
                "## Topik Utama\n"
                "## Konsep Penting (5-8 butir)\n"
                "## Istilah Kunci\n"
                "## Hubungan Antar-Konsep\n"
                "## Bagian yang Berpotensi Membingungkan",
            ),
        ]
    )

    summary_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Anda adalah tutor akademik. Ringkas materi tanpa menghilangkan "
                "gagasan inti dan tanpa membuat referensi palsu.",
            ),
            (
                "human",
                "Topik: {subject}\n"
                "Kesulitan: {difficulty}\n\n"
                "Materi asli:\n{source_text}\n\n"
                "Analisis sebelumnya:\n{analysis}\n\n"
                "Tulis ringkasan terstruktur dengan format:\n"
                "# Ringkasan\n"
                "## Gambaran Umum\n"
                "## Poin Inti\n"
                "## Contoh atau Aplikasi\n"
                "## Kesimpulan\n"
                "Panjang ideal 350-550 kata.",
            ),
        ]
    )

    quiz_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Anda adalah pembuat evaluasi pembelajaran. Semua soal harus dapat "
                "dijawab berdasarkan materi yang diberikan.",
            ),
            (
                "human",
                "Topik: {subject}\n"
                "Tingkat kesulitan: {difficulty}\n\n"
                "Materi:\n{source_text}\n\n"
                "Ringkasan:\n{summary}\n\n"
                "Buat 5 soal pilihan ganda. Setiap soal wajib memiliki opsi A-D, "
                "jawaban benar, dan pembahasan singkat. Gunakan format Markdown "
                "yang konsisten.",
            ),
        ]
    )

    review_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Anda adalah quality assurance untuk keluaran sistem NLP. Nilai "
                "kesetiaan terhadap materi, kelengkapan, kejelasan, dan kualitas soal.",
            ),
            (
                "human",
                "Materi asli:\n{source_text}\n\n"
                "Analisis:\n{analysis}\n\n"
                "Ringkasan:\n{summary}\n\n"
                "Kuis:\n{quiz}\n\n"
                "Berikan penilaian dengan format ketat:\n"
                "SCORE: <angka 0-100>\n"
                "KEKUATAN:\n- ...\n"
                "PERBAIKAN:\n- ...\n"
                "Pastikan baris pertama selalu SCORE.",
            ),
        ]
    )

    revise_summary_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Anda memperbaiki ringkasan akademik berdasarkan evaluasi. "
                "Pertahankan informasi yang benar dan hilangkan klaim yang tidak didukung.",
            ),
            (
                "human",
                "Materi asli:\n{source_text}\n\n"
                "Ringkasan lama:\n{summary}\n\n"
                "Evaluasi:\n{review}\n\n"
                "Tulis versi ringkasan yang telah diperbaiki dalam Markdown.",
            ),
        ]
    )

    revise_quiz_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Anda memperbaiki soal evaluasi agar akurat, jelas, dan sesuai materi.",
            ),
            (
                "human",
                "Materi asli:\n{source_text}\n\n"
                "Kuis lama:\n{quiz}\n\n"
                "Evaluasi:\n{review}\n\n"
                "Tulis ulang 5 soal pilihan ganda dengan opsi A-D, jawaban, dan pembahasan.",
            ),
        ]
    )

    return StudyChains(
        analysis=analysis_prompt | llm | parser,
        summary=summary_prompt | llm | parser,
        quiz=quiz_prompt | llm | parser,
        review=review_prompt | llm | parser,
        revise_summary=revise_summary_prompt | llm | parser,
        revise_quiz=revise_quiz_prompt | llm | parser,
    )
