# Architecture (Phase 5)

## Performance
- Added `PerformanceTracker` for fps, dropped-frame, queue pressure, and per-stage timing.
- Stream pipeline records stage timings for capture, lipsync, encode, OBS output.

## Security
- Optional API token guard for control routes.
- Optional CORS allowlist.
- Safe path utility for preview path boundary checks.

## Deployment and workers
- Worker mode abstraction: `local`, `subprocess` (placeholder), `remote` (health probe + guarded behavior).
- Remote worker client and mode resolver integrated into diagnostics.
