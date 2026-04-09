# Architecture (Phase 3)

## Backend stream pipeline
- `StreamPipeline` manages continuous worker loops:
  - capture loop
  - audio ingestion loop
  - lipsync inference loop
  - publisher loop
- Uses bounded async queues (`FrameQueue`, `AudioQueue`) with frame-drop/backpressure behavior.
- Tracks sync drift via `AVSyncEstimator` and exposes `StreamMetrics`.

## LipSync engine adapters
`LipSyncService` selects engine by config:
- `mock`
- `ffmpeg`
- `wav2lip` (guarded)
- `musetalk` (guarded)
- `liveportrait` (guarded)

On engine failure, service enters degraded mode and falls back to mock engine.

## Preview/stream delivery
- Backward-compatible chunk preview endpoints remain.
- Stream mode adds:
  - latest frame endpoint
  - MJPEG endpoint
  - stream status/start/stop APIs

## OBS output
- `media_source_refresh` mode (works now): refreshes OBS media source with latest frame file.
- `browser_source_url` mode (works when source supports URL): points OBS to local stream endpoint.
