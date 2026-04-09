from __future__ import annotations

from pathlib import Path

from app.core.frame_queue import FramePacket
from app.models.webcam import PreviewChunk
from app.services.lipsync_engines.base import BaseLipSyncEngine, EngineFrameResult


class LivePortraitEngine(BaseLipSyncEngine):
    name = "liveportrait"

    def __init__(self, enabled: bool) -> None:
        self._enabled = enabled

    async def process_frame(self, frame: FramePacket, audio_bytes: bytes | None = None) -> EngineFrameResult:  # noqa: ARG002
        if not self._enabled:
            raise RuntimeError("LivePortrait engine disabled (set ENABLE_EXPERIMENTAL_ENGINES=true)")
        raise NotImplementedError("TODO: integrate LivePortrait inference worker")

    async def render_chunk(self, audio_path: Path, frame_path: Path, output_dir: Path, source: str = "webcam") -> PreviewChunk:  # noqa: ARG002
        if not self._enabled:
            raise RuntimeError("LivePortrait engine disabled")
        raise NotImplementedError("TODO: integrate LivePortrait chunk rendering")
