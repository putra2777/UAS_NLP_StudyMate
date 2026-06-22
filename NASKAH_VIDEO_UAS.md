# Naskah dan Rundown Video UAS NLP

Target durasi: **36-42 menit**. Gunakan naskah ini sebagai panduan, bukan dibaca dengan nada datar. Video wajib memiliki subtitle.

## 00:00-01:30 — Pembukaan

Perkenalkan nama, NIM, kelas, mata kuliah, dan judul proyek **NLP StudyMate**. Jelaskan bahwa proyek menggunakan tiga library wajib: LangChain, LangGraph, dan LangSmith.

Contoh narasi:

> Pada video ini saya akan menjelaskan teori dan implementasi tiga library utama dalam pengembangan aplikasi LLM, yaitu LangChain, LangGraph, dan LangSmith. Setelah bagian teori, saya akan mendemonstrasikan NLP StudyMate, yaitu sistem yang mengubah materi kuliah menjadi analisis, ringkasan, kuis, serta melakukan evaluasi kualitas secara otomatis.

## 01:30-07:30 — Teori LangChain

Bahas poin berikut:

1. LangChain adalah framework untuk menyusun komponen aplikasi LLM.
2. Komponen yang digunakan pada proyek: `ChatPromptTemplate`, model Gemini, dan `StrOutputParser`.
3. Konsep chain dengan operator pipe `|`.
4. Alasan menggunakan prompt berbeda untuk analisis, ringkasan, kuis, review, dan revisi.
5. Tunjukkan `src/chains.py`.

Potongan kode yang perlu ditampilkan:

```python
analysis_prompt | llm | parser
```

Jelaskan bahwa pipeline menerima dictionary input, membentuk prompt, memanggil model, lalu mengubah output menjadi string.

## 07:30-14:30 — Teori LangGraph

Bahas poin berikut:

1. LangGraph mengatur workflow sebagai graph.
2. Node adalah unit proses.
3. Edge adalah hubungan antar-node.
4. State menyimpan data selama workflow.
5. Conditional edge memilih jalur berdasarkan kondisi.
6. Loop revisi menunjukkan bahwa alur tidak hanya linear.

Tampilkan `src/state.py` dan `src/graph.py`.

Jelaskan alurnya:

```text
validate -> analyze -> summarize -> quiz -> review
                                      ^          |
                                      |-- revise-|
```

Terangkan bahwa jika skor di bawah threshold, hasil masuk ke node revisi lalu dinilai kembali.

## 14:30-20:30 — Teori LangSmith

Bahas poin berikut:

1. LangSmith adalah platform observabilitas dan evaluasi aplikasi LLM.
2. Trace menampilkan urutan run, input, output, durasi, dan error.
3. Tags dan metadata memudahkan pengelompokan run.
4. LangSmith membantu menemukan prompt yang gagal atau node yang lambat.
5. Tunjukkan konfigurasi `.env` tanpa memperlihatkan API key lengkap.

Konfigurasi yang ditampilkan:

```env
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=uas-nlp-studymate
```

## 20:30-23:30 — Deskripsi Proyek

Jelaskan masalah yang diselesaikan:

- Mahasiswa sering memiliki materi panjang.
- Ringkasan manual membutuhkan waktu.
- Soal latihan belum tentu tersedia.
- Hasil LLM perlu diperiksa kualitasnya.

Jelaskan solusi:

- Materi dianalisis.
- Sistem menghasilkan ringkasan dan kuis.
- Quality reviewer memberi skor.
- LangGraph merevisi output ketika skor rendah.
- LangSmith mencatat seluruh proses.

## 23:30-27:00 — Struktur Source Code

Tampilkan repository dan jelaskan:

- `app.py`: antarmuka Streamlit.
- `src/chains.py`: pipeline LangChain.
- `src/graph.py`: workflow LangGraph.
- `src/state.py`: struktur state.
- `src/config.py`: konfigurasi environment.
- `data/sample_materi.txt`: materi demo.
- `tests/test_workflow.py`: pengujian fungsi dasar.

## 27:00-34:00 — Demo Aplikasi

Urutan demo:

1. Jalankan `streamlit run app.py`.
2. Tunjukkan status API key dan LangSmith.
3. Pilih tingkat kesulitan.
4. Masukkan materi contoh.
5. Klik **Jalankan Workflow**.
6. Buka tab hasil.
7. Tunjukkan quality score dan jumlah revisi.
8. Jelaskan analisis materi.
9. Jelaskan ringkasan.
10. Tunjukkan lima soal dan pembahasan.
11. Tampilkan quality review.
12. Unduh hasil Markdown.

Kalimat penting:

> Hasil ini tidak dibuat oleh satu prompt saja. Ada beberapa chain yang dijalankan sebagai node terpisah. LangGraph mempertahankan state dari satu node ke node berikutnya, sedangkan LangSmith mencatat seluruh eksekusi.

## 34:00-38:00 — Demo LangSmith

Buka dashboard LangSmith dan pilih project `uas-nlp-studymate`.

Tunjukkan:

1. Parent run workflow.
2. Child run analisis.
3. Child run ringkasan.
4. Child run kuis.
5. Child run review.
6. Node revisi bila muncul.
7. Input dan output salah satu run.
8. Latency dan status run.
9. Tags serta metadata.

Jangan menampilkan API key.

## 38:00-40:30 — Kelebihan, Keterbatasan, dan Pengembangan

Kelebihan:

- Workflow modular.
- Ada quality control.
- Ada conditional loop.
- Dapat ditelusuri melalui LangSmith.

Keterbatasan:

- Bergantung pada model dan API.
- Quality score tetap berasal dari model sehingga bukan ukuran mutlak.
- Materi yang buruk dapat menghasilkan output yang buruk.

Pengembangan:

- Upload PDF.
- RAG dengan vector database.
- Penyimpanan riwayat.
- Evaluasi dataset di LangSmith.
- Multi-user authentication.

## 40:30-41:30 — Penutup

Simpulkan:

> LangChain digunakan untuk membangun komponen pemrosesan LLM, LangGraph digunakan untuk mengontrol workflow dan revisi, sedangkan LangSmith digunakan untuk tracing dan observabilitas. Ketiganya saling melengkapi dalam membangun aplikasi NLP yang modular dan dapat dievaluasi.

Tutup video dan pastikan subtitle telah terpasang.

## Checklist Sebelum Rekam

- `.env` sudah benar.
- API key tidak tampil pada layar.
- LangSmith menerima trace.
- Aplikasi berjalan tanpa error.
- Materi demo telah disiapkan.
- Browser dan font cukup besar.
- Repository GitHub sudah public.
- README sudah menampilkan screenshot aktual.
