from __future__ import annotations

from pathlib import Path


class LipSyncService:
    """Phase 2 placeholder service.

    TODO: wire webcam/avatar frames + Wav2Lip-like chunk pipeline.
    """

    async def render_chunk(self, audio_path: Path, avatar_source: str | None = None) -> Path:
        # MVP stub: returns input audio path to keep interface stable.
        return audio_path
