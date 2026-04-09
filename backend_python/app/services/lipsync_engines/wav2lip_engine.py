from __future__ import annotations

from pathlib import Path

from app.core.frame_queue import FramePacket
from app.models.webcam import PreviewChunk
from app.services.lipsync_engines.base import BaseLipSyncEngine, EngineFrameResult


class Wav2LipEngine(BaseLipSyncEngine):
    name = "wav2lip"

    def __init__(self, enabled: bool) -> None:
        self._enabled = enabled

    async def process_frame(self, frame: FramePacket, audio_bytes: bytes | None = None) -> EngineFrameResult:  # noqa: ARG002
        if not self._enabled:
            raise RuntimeError("Wav2Lip engine disabled (set ENABLE_EXPERIMENTAL_ENGINES=true)")
        raise NotImplementedError("TODO: integrate actual Wav2Lip inference worker")

    async def render_chunk(self, audio_path: Path, frame_path: Path, output_dir: Path, source: str = "webcam") -> PreviewChunk:  # noqa: ARG002
        if not self._enabled:
            raise RuntimeError("Wav2Lip engine disabled")
        raise NotImplementedError("TODO: integrate actual Wav2Lip chunk rendering")
