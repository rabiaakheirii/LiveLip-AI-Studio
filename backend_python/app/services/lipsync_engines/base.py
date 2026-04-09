from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from app.core.frame_queue import FramePacket
from app.models.webcam import PreviewChunk


@dataclass
class EngineFrameResult:
    seq_id: int
    ts: datetime
    jpeg_bytes: bytes
    engine: str


class BaseLipSyncEngine(ABC):
    name: str

    @abstractmethod
    async def process_frame(self, frame: FramePacket, audio_bytes: bytes | None = None) -> EngineFrameResult:
        raise NotImplementedError

    @abstractmethod
    async def render_chunk(self, audio_path: Path, frame_path: Path, output_dir: Path, source: str = "webcam") -> PreviewChunk:
        raise NotImplementedError
