# LiveLip-AI-Studio

Local-first monorepo for real-time(ish) lipsync assistant with Flutter desktop UI and FastAPI backend.

## Architecture overview
- Flutter desktop app = controller/monitor UI.
- FastAPI backend = orchestration + workers + APIs + websocket events.
- Phase 4 hardening adds reliability boundaries, diagnostics APIs, structured logging, tests, scripts, and packaging support.

## Feature matrix
### Working now
- Phase 1+2+3 APIs and UI remain compatible.
- Stream pipeline worker loops with bounded queues.
- Stream metrics/events and diagnostics summary.
- MJPEG/latest-frame preview endpoints.
- OBS output modes: media-source refresh and browser-source URL.

### Fallback/degraded
- Engine fallback to mock when experimental engines fail.
- Webcam mock frame fallback when camera/OpenCV unavailable.

### Placeholder/experimental
- True Wav2Lip/MuseTalk/LivePortrait inference integrations.
- Production-grade distributed deployment and hardened auth.

## External dependencies
- FFmpeg
- Ollama (optional but needed for live LLM path)
- OBS + obs-websocket (optional)
- webcam permission/device access

## Install & run (Ubuntu)
```bash
cp .env.example .env
cd backend_python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

```bash
cd frontend_flutter
flutter pub get
flutter run -d linux
```

## Install & run (Windows PowerShell)
```powershell
copy .env.example .env
cd backend_python
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

```powershell
cd frontend_flutter
flutter pub get
flutter run -d windows
```

## Tests
### Backend
```bash
./scripts/test_backend.sh
```

### Flutter
```bash
./scripts/test_flutter.sh
```

### Smoke test (backend running)
```bash
./scripts/smoke_test.sh
```

## Troubleshooting
- `pip` timeout on OpenCV: retry with higher timeout or temporarily install without OpenCV for mock mode.
- No camera: backend falls back to mock frame.
- No `ffmpeg`: preview rendering/stream quality is limited.
- OBS not connected: system continues with non-OBS fallback.

## Packaging notes
- Backend Docker support: `backend_python/Dockerfile`
- Dev compose: `docker-compose.dev.yml`
- Flutter desktop builds are platform-specific; use `flutter build linux` / `flutter build windows`.

## Runtime directories
- runtime/audio
- runtime/frames
- runtime/preview
- runtime/cache

## Roadmap after Phase 4
- Phase 5: performance optimization, real model workers, deployment security, and remote/multi-machine execution.
