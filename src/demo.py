from __future__ import annotations

from src.state import StudyState


def run_demo_workflow(state: StudyState) -> StudyState:
    """Return deterministic sample output when DEMO_MODE is enabled."""
    subject = state.get("subject", "Natural Language Processing")
    source = state.get("source_text", "")
    excerpt = source[:280].strip() or "Materi contoh belum diisi."

    analysis = f"""## Topik Utama
{subject}

## Konsep Penting
- Materi diproses melalui tahapan analisis, peringkasan, pembuatan kuis, dan evaluasi.
- LangChain menyusun prompt dan pemanggilan model.
- LangGraph mengatur alur node, state, percabangan, dan revisi.
- LangSmith mencatat trace untuk observabilitas.

## Istilah Kunci
NLP, LLM, prompt, chain, graph, state, tracing.

## Hubungan Antar-Konsep
LangChain menjadi komponen pemrosesan, LangGraph menjadi orkestrator, dan LangSmith menjadi lapisan pemantauan.

## Bagian yang Berpotensi Membingungkan
Perbedaan antara chain linear dan graph yang memiliki percabangan atau perulangan.
"""

    summary = f"""# Ringkasan

## Gambaran Umum
Materi **{subject}** dianalisis dengan workflow adaptif. Potongan materi yang diterima sistem adalah: “{excerpt}...”

## Poin Inti
Sistem mengubah teks sumber menjadi analisis terstruktur, ringkasan, dan kuis. Setelah itu, node quality review memberi skor. Jika skor belum memenuhi batas, LangGraph mengarahkan hasil ke node revisi sebelum finalisasi.

## Contoh atau Aplikasi
Workflow dapat digunakan untuk materi kuliah, modul pelatihan, atau catatan pembelajaran.

## Kesimpulan
Kombinasi ketiga library memisahkan fungsi pemrosesan LLM, orkestrasi workflow, dan observabilitas.
"""

    quiz = """### Soal 1
Apa fungsi utama LangGraph pada proyek ini?

A. Menyimpan file PDF  
B. Mengatur alur node dan state  
C. Membuat akun pengguna  
D. Menggambar antarmuka

**Jawaban: B**  
**Pembahasan:** LangGraph mengatur node, edge, state, percabangan, dan perulangan.

### Soal 2
Library yang digunakan untuk tracing adalah ...

A. Streamlit  
B. Pydantic  
C. LangSmith  
D. Pytest

**Jawaban: C**  
**Pembahasan:** LangSmith menyediakan observabilitas terhadap proses pemanggilan model dan workflow.

### Soal 3
Apa yang dilakukan node review?

A. Menghapus source code  
B. Menilai kualitas hasil  
C. Mengganti API key  
D. Menutup aplikasi

**Jawaban: B**  
**Pembahasan:** Node review menilai akurasi, kelengkapan, kejelasan, dan kualitas kuis.

### Soal 4
Kapan node revisi dijalankan?

A. Saat skor di bawah threshold  
B. Setiap aplikasi dibuka  
C. Sebelum input diberikan  
D. Saat repository dibuat

**Jawaban: A**  
**Pembahasan:** Conditional edge mengarahkan workflow ke revisi apabila skor belum memenuhi batas.

### Soal 5
Apa peran LangChain?

A. Menyusun prompt dan pipeline model  
B. Mengelola database relasional  
C. Membuat desain logo  
D. Mengunggah video

**Jawaban: A**  
**Pembahasan:** LangChain menghubungkan prompt, model, dan output parser.
"""

    review = """SCORE: 92
KEKUATAN:
- Alur ketiga library terlihat jelas.
- Ringkasan dan kuis konsisten dengan konsep proyek.
PERBAIKAN:
- Pada penggunaan nyata, tambahkan materi yang lebih panjang agar evaluasi lebih representatif.
"""

    return {
        **state,
        "analysis": analysis,
        "summary": summary,
        "quiz": quiz,
        "review": review,
        "quality_score": 92,
        "revision_count": 0,
        "final_output": f"{summary}\n\n# Kuis\n\n{quiz}",
        "error": "",
    }
