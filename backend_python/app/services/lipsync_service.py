from __future__ import annotations

import logging
from pathlib import Path

from app.core.frame_queue import FramePacket
from app.models.webcam import PreviewChunk
from app.services.lipsync_engines.base import BaseLipSyncEngine, EngineFrameResult
from app.services.lipsync_engines.ffmpeg_engine import FFmpegLipSyncEngine
from app.services.lipsync_engines.liveportrait_engine import LivePortraitEngine
from app.services.lipsync_engines.mock_engine import MockLipSyncEngine
from app.services.lipsync_engines.musetalk_engine import MuseTalkEngine
from app.services.lipsync_engines.wav2lip_engine import Wav2LipEngine

logger = logging.getLogger(__name__)


class LipSyncService:
    def __init__(self, preview_dir: Path, engine_name: str = "ffmpeg", experimental_enabled: bool = False) -> None:
        self._preview_dir = preview_dir
        self._engine_name = engine_name
        self._experimental_enabled = experimental_enabled
        self._engine: BaseLipSyncEngine = self._build_engine(engine_name)
        self.degraded_mode = False

    @property
    def engine_name(self) -> str:
        return self._engine.name

    def _build_engine(self, engine_name: str) -> BaseLipSyncEngine:
        try:
            if engine_name == "ffmpeg":
                return FFmpegLipSyncEngine()
            if engine_name == "wav2lip":
                return Wav2LipEngine(enabled=self._experimental_enabled)
            if engine_name == "musetalk":
                return MuseTalkEngine(enabled=self._experimental_enabled)
            if engine_name == "liveportrait":
                return LivePortraitEngine(enabled=self._experimental_enabled)
            return MockLipSyncEngine()
        except Exception:
            logger.exception("Failed to initialize lipsync engine=%s; using mock", engine_name)
            self.degraded_mode = True
            return MockLipSyncEngine()

    async def process_frame(self, frame: FramePacket, audio_bytes: bytes | None = None) -> EngineFrameResult:
        try:
            return await self._engine.process_frame(frame, audio_bytes)
        except Exception as exc:
            logger.warning("process_frame failed in %s: %s; falling back to mock", self._engine.name, exc)
            self.degraded_mode = True
            fallback = MockLipSyncEngine()
            return await fallback.process_frame(frame, audio_bytes)

    async def render_chunk(self, audio_path: Path, frame_path: Path, source: str = "webcam") -> PreviewChunk:
        try:
            return await self._engine.render_chunk(audio_path, frame_path, self._preview_dir, source=source)
        except Exception as exc:
            logger.warning("render_chunk failed in %s: %s; falling back to mock", self._engine.name, exc)
            self.degraded_mode = True
            fallback = MockLipSyncEngine()
            return await fallback.render_chunk(audio_path, frame_path, self._preview_dir, source=source)
