# LiveLip-AI-Studio (Phase 5)

FastAPI + Flutter local-first lipsync platform with streaming, diagnostics, security guards, performance metrics, and worker-mode abstractions.

## Feature matrix
### Working now
- Phase 1-4 compatibility preserved.
- Stream worker pipeline with queue pressure and AV drift metrics.
- Performance metrics endpoint and Flutter diagnostics panel.
- Optional API token guard for control routes.
- Worker mode abstraction (local implemented, remote/subprocess routed as guarded modes).

### Fallback mode
- mock/ffmpeg engine fallback and degraded mode.
- webcam fallback frame when camera unavailable.

### Experimental/dependency-gated
- real Wav2Lip/MuseTalk/LivePortrait execution.
- remote worker full execution path (health contract implemented, full RPC not).

## Run (Ubuntu)
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

## Run (Windows)
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
```bash
./scripts/test_backend.sh
./scripts/test_flutter.sh
./scripts/smoke_test.sh
```

## Key docs
- `docs/architecture.md`
- `docs/testing.md`
- `docs/deployment.md`
- `docs/deployment_modes.md`
- `docs/security.md`
- `docs/lipsync_engines.md`
