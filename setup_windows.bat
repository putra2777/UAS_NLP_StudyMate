@echo off
setlocal

if not exist .venv (
    py -m venv .venv
)

call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

if not exist .env (
    copy .env.example .env
    echo File .env dibuat. Silakan isi GOOGLE_API_KEY dan LANGSMITH_API_KEY.
)

echo.
echo Instalasi selesai.
echo Jalankan: run_windows.bat
pause
