#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(dirname "$0")/.."

bash "$ROOT_DIR/scripts/run_backend.sh" &
BACK_PID=$!

sleep 3
bash "$ROOT_DIR/scripts/run_flutter.sh"

kill "$BACK_PID" || true
