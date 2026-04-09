# flutter_live_lipsync_assistant Architecture

## Monorepo layout
- `frontend_flutter/`: Flutter desktop app (Linux/Windows first).
- `backend_python/`: FastAPI control plane + local worker adapters.
- `shared_protocol/`: JSON schema and protocol notes.
- `scripts/`: local run scripts.
- `docs/`: design docs and phase plan.

## Phase plan
1. **Phase 1 (implemented skeleton)**: Mic->STT->Ollama->TTS->OBS audio + Flutter transcript/response/status.
2. **Phase 2**: Webcam capture + chunked lip-sync rendering + preview endpoint.
3. **Phase 3**: Near real-time streaming lip-sync output to OBS.

## State machine
`idle -> listening -> transcribing -> thinking -> speaking -> lip_syncing -> streaming -> error`

Current MVP transitions currently use `streaming` directly after `speaking`; `lip_syncing` service is exposed and ready for Phase 2 wiring.
