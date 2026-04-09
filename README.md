# flutter_live_lipsync_assistant (Local-first MVP)

Phase 1 + Phase 2 scaffold for a Flutter-controlled local pipeline:
Mic -> STT -> Ollama -> TTS -> webcam frame capture -> chunk preview render -> OBS media-source update.

## Updated project tree

```text
.
├── .env.example
├── README.md
├── backend_python
│   ├── app
│   │   ├── api
│   │   │   ├── routes_pipeline.py
│   │   │   ├── routes_preview.py
│   │   │   ├── routes_settings.py
│   │   │   └── routes_webcam.py
│   │   ├── core
│   │   │   ├── config.py
│   │   │   ├── events.py
│   │   │   ├── orchestrator.py
│   │   │   ├── state_machine.py
│   │   │   └── storage_paths.py
│   │   ├── dependencies.py
│   │   ├── main.py
│   │   ├── models
│   │   │   └── webcam.py
│   │   └── services
│   │       ├── lipsync_service.py
│   │       ├── obs_service.py
│   │       ├── ollama_service.py
│   │       ├── render_queue_service.py
│   │       ├── stt_service.py
│   │       ├── tts_service.py
│   │       └── webcam_service.py
│   └── requirements.txt
├── docs
│   └── architecture.md
├── frontend_flutter
│   ├── lib
│   │   ├── main.dart
│   │   ├── models
│   │   │   ├── ai_response.dart
│   │   │   ├── app_state.dart
│   │   │   ├── camera_device.dart
│   │   │   ├── pipeline_status.dart
│   │   │   ├── preview_chunk.dart
│   │   │   └── transcript_chunk.dart
│   │   ├── providers
│   │   │   └── preview_provider.dart
│   │   ├── screens
│   │   │   ├── dashboard_screen.dart
│   │   │   ├── logs_screen.dart
│   │   │   ├── response_screen.dart
│   │   │   ├── settings_screen.dart
│   │   │   └── transcript_screen.dart
│   │   ├── services
│   │   │   ├── api_service.dart
│   │   │   └── websocket_service.dart
│   │   ├── state
│   │   │   └── app_controller.dart
│   │   └── widgets
│   │       ├── camera_selector.dart
│   │       ├── control_bar.dart
│   │       ├── obs_status_card.dart
│   │       ├── preview_panel.dart
│   │       ├── preview_status_card.dart
│   │       ├── response_panel.dart
│   │       ├── status_badge.dart
│   │       └── transcript_panel.dart
│   └── pubspec.yaml
├── scripts
│   ├── run_backend.sh
│   ├── run_dev_all.sh
│   └── run_flutter.sh
└── shared_protocol
    └── websocket_events.json
```

## Phase 2 architecture decisions (concise)

1. Webcam capture is abstracted via `WebcamService` with list/select/capture methods and mock fallback.
2. Rendering is queue/history-backed and chunk-based (`RenderQueueService` + `LipSyncService`).
3. `LipSyncService` now produces preview MP4 chunks via FFmpeg shell (placeholder for true lip-sync models).
4. Preview assets are exposed through REST metadata and static file serving (`/api/preview/*` + `/preview/<file>`).
5. Existing Phase 1 orchestration remains, with additional states/events layered in without removing old ones.

## REST + WS updates

### New REST endpoints
- `GET /api/webcam/devices`
- `POST /api/webcam/select`
- `GET /api/preview/latest`
- `GET /api/preview/history`
- `GET /preview/<file>` (static files)

### New websocket event types
- `camera_list`
- `camera_selected`
- `preview_chunk_ready`
- `preview_status`
- `render_progress`
- `render_error`

## Ubuntu run commands

```bash
# 1) prerequisites
sudo apt update
sudo apt install -y python3 python3-venv ffmpeg

# 2) backend
cd backend_python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# 3) frontend (new terminal)
cd frontend_flutter
flutter pub get
flutter run -d linux
```

## Windows run commands (PowerShell)

```powershell
# 1) backend
cd backend_python
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# 2) frontend (new terminal)
cd frontend_flutter
flutter pub get
flutter run -d windows
```

## What works now

- Phase 1 pipeline skeleton remains working.
- Camera discovery/selection endpoints and websocket camera events.
- Snapshot capture from selected webcam (or mock fallback).
- FFmpeg chunk render shell that combines frame + TTS audio into an MP4 preview chunk.
- Preview metadata/history endpoints and preview file serving.
- Flutter dashboard/settings now show camera selector, preview status/progress, and recent preview chunks.
- OBS audio push still works; preview video media-source update hook added.

## Placeholder/TODO (honest)

- True lip movement generation is **not** implemented yet.
- Webcam is currently sampled frame capture (not continuous stream processing).
- Flutter currently displays preview URLs/history, not an embedded video player.
- OBS video path update is media-source refresh, not low-latency live transport.

## Phase 3 prompt starter

Use this prompt for the next implementation pass:

> Implement Phase 3 near-real-time lip-sync streaming for flutter_live_lipsync_assistant. Keep existing architecture. Add continuous webcam capture, bounded render/encode queues, incremental TTS chunking, near-real-time lip-sync model worker integration, low-latency preview stream endpoint, and OBS live video injection adapter (RTMP/virtual-cam/NDI abstraction). Include frame/audio latency metrics, backpressure handling, and reconnection logic.
