# Deployment Notes (Phase 5)

## Local safest mode
- bind to `127.0.0.1`
- leave `ALLOW_CORS_ORIGINS` empty
- set `API_AUTH_TOKEN` if using LAN access

## Docker backend
```bash
cd backend_python
docker build -t livelip-backend:dev .
```

```bash
docker compose -f docker-compose.dev.yml up --build
```
