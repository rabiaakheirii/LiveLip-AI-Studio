#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
python -m json.tool shared_protocol/websocket_events.json >/dev/null
echo "protocol json valid"
