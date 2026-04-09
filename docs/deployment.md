# Deployment Notes (Phase 4)

## Backend Docker (optional)
```bash
cd backend_python
docker build -t livelip-backend:dev .
docker run --rm -p 8000:8000 --env-file ../.env livelip-backend:dev
```

## Docker Compose dev
```bash
docker compose -f docker-compose.dev.yml up --build
```

## Flutter desktop packaging
- Linux: `flutter build linux`
- Windows: `flutter build windows`

## External runtime dependencies
- FFmpeg executable in PATH
- Ollama running (if LLM path needed)
- OBS with websocket enabled (if OBS output path needed)
