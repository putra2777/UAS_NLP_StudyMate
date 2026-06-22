# Ringkasan

## Gambaran Umum
Materi **Natural Language Processing** dianalisis dengan workflow adaptif. Potongan materi yang diterima sistem adalah: “Natural Language Processing (NLP) adalah bidang yang mempelajari bagaimana komputer memproses, memahami, dan menghasilkan bahasa manusia. Dalam sistem modern, NLP banyak menggunakan model bahasa besar atau Large Language Model (LLM). Model tersebut mempelajari pola statistik dari...”

## Poin Inti
Sistem mengubah teks sumber menjadi analisis terstruktur, ringkasan, dan kuis. Setelah itu, node quality review memberi skor. Jika skor belum memenuhi batas, LangGraph mengarahkan hasil ke node revisi sebelum finalisasi.

## Contoh atau Aplikasi
Workflow dapat digunakan untuk materi kuliah, modul pelatihan, atau catatan pembelajaran.

## Kesimpulan
Kombinasi ketiga library memisahkan fungsi pemrosesan LLM, orkestrasi workflow, dan observabilitas.


# Kuis

### Soal 1
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


## Quality Review

```text
SCORE: 92
KEKUATAN:
- Alur ketiga library terlihat jelas.
- Ringkasan dan kuis konsisten dengan konsep proyek.
PERBAIKAN:
- Pada penggunaan nyata, tambahkan materi yang lebih panjang agar evaluasi lebih representatif.

```
