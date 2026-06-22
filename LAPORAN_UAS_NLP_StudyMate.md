# Laporan Singkat UAS NLP: NLP StudyMate

## Identitas Mahasiswa

Nama: ........................................  
NIM: .........................................  
Kelas: .......................................  
Mata Kuliah: Natural Language Processing  
Judul Proyek: NLP StudyMate

## 1. Deskripsi Proyek

NLP StudyMate adalah aplikasi asisten belajar adaptif yang mengubah materi kuliah berbentuk teks menjadi analisis konsep, ringkasan terstruktur, kuis pilihan ganda, dan evaluasi kualitas. Proyek ini dirancang untuk menunjukkan implementasi tiga komponen utama dalam pengembangan aplikasi berbasis Large Language Model, yaitu LangChain, LangGraph, dan LangSmith.

Masalah utama yang diangkat adalah kebutuhan mahasiswa untuk memahami materi panjang secara lebih cepat tanpa kehilangan struktur konsep. Dalam praktik belajar, mahasiswa sering membutuhkan ringkasan, latihan soal, dan umpan balik terhadap kualitas materi belajar. Aplikasi ini menjawab kebutuhan tersebut dengan workflow bertahap, bukan hanya satu prompt tunggal.

## 2. Tujuan Proyek

Tujuan proyek ini adalah membangun prototipe aplikasi NLP yang mampu memproses materi teks menjadi keluaran pembelajaran yang lebih terstruktur. Secara teknis, proyek ini juga bertujuan memperlihatkan bagaimana LangChain digunakan untuk membangun pipeline prompt-model-parser, LangGraph digunakan untuk mengatur alur kerja berbasis state dan conditional routing, serta LangSmith digunakan untuk menelusuri proses eksekusi model.

## 3. Teknologi yang Digunakan

Aplikasi dikembangkan menggunakan Python dan Streamlit sebagai antarmuka pengguna. Integrasi model bahasa dilakukan melalui LangChain dengan model Google Gemini. Workflow dibangun menggunakan LangGraph agar setiap tahap pemrosesan dapat dipisahkan menjadi node yang jelas. Observabilitas proses dilakukan melalui LangSmith agar input, output, durasi, metadata, dan urutan eksekusi dapat diperiksa saat demo.

## 4. Arsitektur Sistem

Workflow aplikasi dimulai dari validasi input. Jika materi terlalu pendek, sistem menghentikan proses dan menampilkan pesan kesalahan. Jika input valid, sistem menjalankan node analisis materi, pembuatan ringkasan, pembuatan kuis, dan quality review. Skor quality review digunakan sebagai dasar percabangan. Jika skor belum mencapai threshold, LangGraph mengarahkan output ke node revisi, kemudian hasil yang telah direvisi dinilai ulang.

Alur sistem dapat diringkas sebagai berikut:

```text
START
  -> Validate Input
  -> Analyze Material
  -> Generate Summary
  -> Generate Quiz
  -> Quality Review
       -> jika skor rendah: Revise Output -> Quality Review
       -> jika skor cukup: Finalize
  -> END
```

## 5. Implementasi LangChain

LangChain digunakan pada file `src/chains.py`. Setiap fungsi utama aplikasi dibuat sebagai chain tersendiri, yaitu chain analisis, chain ringkasan, chain kuis, chain review, chain revisi ringkasan, dan chain revisi kuis. Pendekatan ini membuat prompt lebih mudah dikontrol karena setiap tahap memiliki instruksi yang spesifik.

Contoh implementasi chain adalah penggunaan `ChatPromptTemplate`, model Gemini, dan `StrOutputParser` dalam satu pipeline. Dengan pola ini, input dari pengguna diterima sebagai dictionary, kemudian diubah menjadi prompt, dikirim ke model, dan hasilnya dikembalikan sebagai string Markdown.

## 6. Implementasi LangGraph

LangGraph digunakan pada file `src/graph.py` untuk membangun workflow berbasis graph. Setiap proses aplikasi direpresentasikan sebagai node. Perpindahan antarproses direpresentasikan sebagai edge. Data yang bergerak antar-node disimpan dalam `StudyState` pada file `src/state.py`.

Keunggulan utama implementasi LangGraph dalam proyek ini adalah conditional routing. Setelah quality review menghasilkan skor, sistem memutuskan apakah output langsung difinalisasi atau perlu direvisi. Dengan demikian, alur aplikasi tidak bersifat linear sepenuhnya, melainkan adaptif terhadap kualitas keluaran.

## 7. Implementasi LangSmith

LangSmith digunakan sebagai lapisan observabilitas. Pada saat aplikasi dijalankan dengan API key yang valid, setiap chain dan workflow diberi `run_name`, `tags`, dan `metadata`. Informasi ini memudahkan demonstrasi karena setiap tahap eksekusi dapat ditelusuri melalui dashboard LangSmith.

Bagian yang dapat ditunjukkan dalam video adalah parent run workflow, child run untuk analisis, ringkasan, kuis, quality review, serta node revisi jika muncul. Mahasiswa juga dapat menunjukkan durasi eksekusi, input-output tiap run, dan metadata seperti topik serta tingkat kesulitan.

## 8. Fitur Aplikasi

Aplikasi memiliki fitur input materi, pemilihan tingkat kesulitan, analisis topik utama, ringkasan terstruktur, pembuatan lima soal pilihan ganda, quality review berbasis skor, revisi otomatis, unduh hasil Markdown, serta mode demo. Mode demo hanya digunakan untuk melihat antarmuka tanpa API key. Untuk demonstrasi final, aplikasi sebaiknya dijalankan dengan `DEMO_MODE=false` agar hasil benar-benar diproses oleh model.

## 9. Pengujian

Pengujian unit dilakukan pada fungsi utilitas yang tidak membutuhkan API eksternal. Fungsi yang diuji meliputi parsing skor dari hasil review, validasi input pendek, dan validasi input yang memenuhi panjang minimum. Hasil pengujian lokal menunjukkan seluruh test berhasil dijalankan.

```text
5 passed
```

Pengujian penuh terhadap workflow LLM tetap membutuhkan instalasi dependency, Google Gemini API key, dan LangSmith API key. Tanpa API key, validasi penuh terhadap trace LangSmith tidak dapat dilakukan.

## 10. Keterbatasan

Keterbatasan utama aplikasi adalah ketergantungan terhadap model eksternal dan kualitas input. Quality score yang dihasilkan oleh model tidak dapat diperlakukan sebagai ukuran objektif mutlak karena tetap berasal dari evaluasi LLM. Selain itu, aplikasi belum mendukung upload PDF, penyimpanan riwayat, autentikasi pengguna, dan evaluasi berbasis dataset terstandardisasi.

## 11. Kesimpulan

NLP StudyMate menunjukkan implementasi aplikasi NLP modern yang memisahkan pemrosesan LLM, orkestrasi workflow, dan observabilitas. LangChain berperan dalam membangun pipeline pemrosesan, LangGraph mengatur alur kerja adaptif berbasis state, sedangkan LangSmith membantu pelacakan dan debugging. Secara fungsional, proyek ini relevan sebagai prototipe asisten belajar karena mampu menghasilkan ringkasan, kuis, serta evaluasi kualitas dari materi kuliah.
