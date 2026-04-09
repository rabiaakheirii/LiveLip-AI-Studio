# flutter_live_lipsync_assistant

Local-first monorepo for Flutter-controlled live lip-sync assistant.

## Phases implemented
- Phase 1: STT -> Ollama -> TTS -> OBS audio skeleton.
- Phase 2: webcam abstraction + chunk preview rendering + preview APIs.
- Phase 3 (this repo state): near-real-time stream architecture with worker loops, queue pressure metrics, MJPEG/latest-frame output, engine adapters, and OBS live-output fallback mode.

## Key routes
- Health: `GET /health`
- Pipeline: `/pipeline/start`, `/pipeline/stop`, `/pipeline/state`
- Webcam: `/api/webcam/devices`, `/api/webcam/select`
- Preview compatibility: `/api/preview/latest`, `/api/preview/history`, `/preview/<file>`
- Stream mode:
  - `POST /api/stream/start`
  - `POST /api/stream/stop`
  - `GET /api/stream/status`
  - `GET /api/stream/latest-frame`
  - `GET /api/stream/mjpeg`

## Run (Ubuntu)
```bash
cp .env.example .env
cd backend_python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

New terminal:
```bash
cd frontend_flutter
flutter pub get
flutter run -d linux
```

## Run (Windows PowerShell)
```powershell
copy .env.example .env
cd backend_python
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

New terminal:
```powershell
cd frontend_flutter
flutter pub get
flutter run -d windows
```

## Stream smoke test
```bash
curl -X POST http://127.0.0.1:8000/api/stream/start
curl http://127.0.0.1:8000/api/stream/status
curl -o latest.jpg http://127.0.0.1:8000/api/stream/latest-frame
curl -X POST http://127.0.0.1:8000/api/stream/stop
```

## Implemented now vs fallback
- Implemented now:
  - continuous worker pipeline with capture/audio/inference/publisher loops
  - bounded queues + backpressure + dropped frame counting
  - MJPEG/latest-frame stream endpoints
  - stream websocket events and metrics
  - OBS live output abstraction with file-refresh/browser-source modes
- Fallback mode:
  - mock lipsync engine and ffmpeg pass-through engine
  - degraded mode when experimental engine fails/unavailable
- Structured TODO:
  - true Wav2Lip/MuseTalk/LivePortrait runtime integration
  - production-grade low-latency transport (WebRTC/RTMP/NDI)
