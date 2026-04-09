#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://127.0.0.1:8000}"

echo "[1/6] health"
curl -fsS "$BASE_URL/health" >/dev/null

echo "[2/6] webcam devices"
curl -fsS "$BASE_URL/api/webcam/devices" >/dev/null

echo "[3/6] stream status"
curl -fsS "$BASE_URL/api/stream/status" >/dev/null

echo "[4/6] diagnostics"
curl -fsS "$BASE_URL/api/diagnostics/summary" >/dev/null

echo "[5/6] start stream"
curl -fsS -X POST "$BASE_URL/api/stream/start" >/dev/null
sleep 1

echo "[6/6] stop stream"
curl -fsS -X POST "$BASE_URL/api/stream/stop" >/dev/null

echo "smoke test passed"
