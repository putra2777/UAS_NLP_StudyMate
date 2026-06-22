# Panduan Pengumpulan Final

## File yang Sudah Siap

Proyek ini sudah berisi source code aplikasi, README, contoh materi, dokumentasi arsitektur, naskah video, template subtitle, dan hasil demo Markdown. Struktur utama sudah cukup untuk diunggah ke GitHub sebagai repository public.

## Yang Harus Diisi Manual

1. Isi identitas mahasiswa pada `LAPORAN_UAS_NLP_StudyMate.md`.
2. Salin `.env.example` menjadi `.env`.
3. Isi `GOOGLE_API_KEY` dari Google AI Studio.
4. Isi `LANGSMITH_API_KEY` dari LangSmith.
5. Jalankan aplikasi dengan `DEMO_MODE=false` untuk demo final.
6. Rekam video 30 sampai 50 menit mengikuti `NASKAH_VIDEO_UAS.md`.
7. Pastikan API key tidak terlihat di video.
8. Upload video ke Google Drive dan buka aksesnya.
9. Upload source code ke GitHub public tanpa file `.env`.
10. Kirim link GitHub dan link Google Drive melalui Google Classroom.

## Perintah Instalasi Windows

```bash
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```

## Perintah Instalasi Linux atau macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

## Perintah Test

```bash
pytest -q
```

Hasil uji lokal pada fungsi utilitas:

```text
5 passed
```

## Catatan Penting

Jangan unggah file `.env` ke GitHub. Jangan memperlihatkan API key ketika merekam video. Jika trace LangSmith belum muncul, pastikan `LANGSMITH_TRACING=true`, `LANGSMITH_API_KEY` sudah benar, dan nama project sesuai dengan `LANGSMITH_PROJECT`.
