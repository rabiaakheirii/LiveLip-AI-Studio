# Architecture Notes (Phase 1 + Phase 2)

## Core principle
Flutter is only the desktop control plane and UI. Heavy operations remain in Python services.

## Backend additions in Phase 2
- `WebcamService`: camera discovery/selection and snapshot capture abstraction.
- `LipSyncService`: FFmpeg-based chunk renderer shell for preview MP4 generation.
- `RenderQueueService`: bounded in-memory history for preview metadata.
- `StoragePaths`: centralized runtime directories (`audio/`, `frames/`, `preview/`, `cache/`).

## Pipeline extension
Phase 1 states are preserved and extended with:
- `camera_ready`
- `capturing_video`
- `rendering_preview`
- `preview_ready`

## Preview transport
- Metadata endpoints: `/api/preview/latest`, `/api/preview/history`
- Static media endpoint: `/preview/<file>`
- WS event: `preview_chunk_ready`

## Future replacement points
- Swap `LipSyncService.render_chunk` with Wav2Lip/MuseTalk/LivePortrait worker.
- Replace OBS file-source updates with low-latency live ingest.
