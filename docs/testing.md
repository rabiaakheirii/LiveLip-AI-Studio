# Testing Guide (Phase 4)

## Backend tests
```bash
./scripts/test_backend.sh
```

## Flutter tests
```bash
./scripts/test_flutter.sh
```

## Smoke tests
```bash
# backend must already be running on localhost:8000
./scripts/smoke_test.sh
```

## Manual checks
- `GET /health`
- `GET /api/diagnostics/summary`
- `POST /api/stream/start`
- `GET /api/stream/status`
- `GET /api/stream/latest-frame`
- `POST /api/stream/stop`
