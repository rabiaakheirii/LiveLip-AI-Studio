#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../backend_python"
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
