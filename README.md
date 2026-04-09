# flutter_live_lipsync_assistant (Local-first MVP)

A monorepo skeleton for a Flutter-controlled live speech -> LLM -> TTS -> OBS pipeline, with a clean split between UI orchestration and local heavy processing.

## Phase-based scope

### Phase 1 (MVP in this repo)
- Local FastAPI orchestration.
- Placeholder STT streaming chunks.
- Ollama response streaming.
- Placeholder TTS (silent WAV generation as replaceable stub).
- OBS websocket connection + media source file update.
- Flutter desktop app with:
  - Start/Stop controls
  - Transcript view
  - Response view
  - Logs view
  - Settings placeholder
  - OBS status card
  - Pipeline health/state display

### Phase 2 (next)
- Webcam capture source.
- Chunked/offline lip sync processing service wiring.
- Local preview endpoint or embedded preview.

### Phase 3 (next)
- Low-latency lip-sync streaming output to OBS.

## Project tree

```text
.
├── .env.example
├── README.md
├── backend_python
│   ├── app
│   │   ├── api
│   │   │   ├── routes_pipeline.py
│   │   │   └── routes_settings.py
│   │   ├── core
│   │   │   ├── config.py
│   │   │   ├── events.py
│   │   │   ├── orchestrator.py
│   │   │   └── state_machine.py
│   │   ├── dependencies.py
│   │   ├── main.py
│   │   └── services
│   │       ├── lipsync_service.py
│   │       ├── obs_service.py
│   │       ├── ollama_service.py
│   │       ├── stt_service.py
│   │       └── tts_service.py
│   ├── requirements.txt
│   └── tests
├── docs
│   └── architecture.md
├── frontend_flutter
│   ├── lib
│   │   ├── main.dart
│   │   ├── models
│   │   │   ├── ai_response.dart
│   │   │   ├── app_state.dart
│   │   │   ├── pipeline_status.dart
│   │   │   └── transcript_chunk.dart
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
│   │       ├── control_bar.dart
│   │       ├── obs_status_card.dart
│   │       ├── response_panel.dart
│   │       ├── status_badge.dart
│   │       └── transcript_panel.dart
│   ├── pubspec.yaml
│   └── test
│       └── widget_test.dart
├── scripts
│   ├── run_backend.sh
│   ├── run_dev_all.sh
│   └── run_flutter.sh
└── shared_protocol
    └── websocket_events.json
```

## WebSocket + REST protocol summary

### WebSocket
- Endpoint: `ws://127.0.0.1:8000/ws/events`
- Message schema: `shared_protocol/websocket_events.json`
- Event types:
  - `pipeline_state`
  - `transcript_partial`
  - `transcript_final`
  - `ai_response_partial`
  - `ai_response_final`
  - `obs_status`
  - `pipeline_timing`
  - `log`
  - `error`

### REST
- `GET /health`
- `POST /pipeline/start`
- `POST /pipeline/stop`
- `GET /pipeline/state`
- `GET /settings`
- `POST /settings`

## Ubuntu setup

1. Install prerequisites:
   - Python 3.11+
   - Flutter SDK (desktop enabled)
   - Ollama
   - OBS + obs-websocket plugin (OBS 28+ has websocket built-in)
2. Clone repo and create env file:
   ```bash
   cp .env.example .env
   ```
3. Start backend:
   ```bash
   ./scripts/run_backend.sh
   ```
4. In another terminal, start Flutter:
   ```bash
   ./scripts/run_flutter.sh
   ```
5. In app, click **Start**.

## Windows setup

1. Install prerequisites:
   - Python 3.11+
   - Flutter SDK with Windows desktop support
   - Visual Studio Build Tools (for Flutter desktop)
   - Ollama for Windows
   - OBS Studio (websocket enabled)
2. Create `.env` from `.env.example`.
3. Backend (PowerShell):
   ```powershell
   cd backend_python
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
4. Frontend (PowerShell):
   ```powershell
   cd frontend_flutter
   flutter pub get
   flutter run -d windows
   ```

## Notes on current stubs
- STT currently emits simulated transcript chunks.
- TTS currently writes a silent WAV placeholder.
- Lip sync currently no-op; service interface is ready for Phase 2 integration.

## Next tasks to make lip sync truly real-time
1. Add mic ring-buffer + VAD + streaming STT (faster-whisper/sherpa-onnx).
2. Implement sentence-level incremental TTS with chunk playback overlap.
3. Build avatar/webcam frame queue + face tracking.
4. Replace `LipSyncService.render_chunk` with Wav2Lip-like worker process and cache.
5. Add FFmpeg graph for muxing TTS audio + lip-synced frames into low-latency stream.
6. Add OBS output adapters (media source update now, RTMP/virtual cam/NDI later).
7. Add backpressure control and QoS metrics (queue lengths, dropped frames, latency budget).
8. Add robust reconnection and retry policies for OBS/Ollama failures.
