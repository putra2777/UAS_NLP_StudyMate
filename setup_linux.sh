#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f .env ]; then
  cp .env.example .env
  echo "File .env dibuat. Isi GOOGLE_API_KEY dan LANGSMITH_API_KEY."
fi

echo "Instalasi selesai. Jalankan ./run.sh"
