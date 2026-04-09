#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../backend_python"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pytest -q
