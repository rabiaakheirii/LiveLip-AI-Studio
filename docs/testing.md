# Testing Guide (Phase 5)

## Backend
```bash
./scripts/test_backend.sh
```

## Flutter
```bash
./scripts/test_flutter.sh
```

## Smoke
```bash
./scripts/smoke_test.sh
```

## Additional checks
- `GET /api/performance/metrics`
- `GET /api/diagnostics/summary`
- protected route checks with/without `X-API-Token` when `API_AUTH_TOKEN` is configured.
