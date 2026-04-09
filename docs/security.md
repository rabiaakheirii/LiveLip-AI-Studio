# Security Notes

## Localhost-only by default
- default host is `127.0.0.1`.

## API token guard
- set `API_AUTH_TOKEN` to protect control routes (`/pipeline`, `/api/stream`, `/api/webcam`).

## CORS
- set explicit `ALLOW_CORS_ORIGINS` list for browser-access scenarios.

## Exposure warning
- this project is not hardened for public internet exposure yet.
