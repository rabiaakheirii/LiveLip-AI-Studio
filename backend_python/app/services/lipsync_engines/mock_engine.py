from __future__ import annotations

import uuid
from datetime import datetime
from pathlib import Path

from app.core.frame_queue import FramePacket
from app.models.webcam import PreviewChunk
from app.services.lipsync_engines.base import BaseLipSyncEngine, EngineFrameResult


class MockLipSyncEngine(BaseLipSyncEngine):
    name = "mock"

    async def process_frame(self, frame: FramePacket, audio_bytes: bytes | None = None) -> EngineFrameResult:  # noqa: ARG002
        return EngineFrameResult(seq_id=frame.seq_id, ts=frame.ts, jpeg_bytes=frame.jpeg_bytes, engine=self.name)

    async def render_chunk(self, audio_path: Path, frame_path: Path, output_dir: Path, source: str = "webcam") -> PreviewChunk:  # noqa: ARG002
        # fallback preview artifact for environments without ffmpeg
        chunk_id = uuid.uuid4().hex[:10]
        file_name = f"preview_{chunk_id}.jpg"
        output_path = output_dir / file_name
        output_path.write_bytes(frame_path.read_bytes() if frame_path.exists() else b"")
        return PreviewChunk(
            chunk_id=chunk_id,
            file_name=file_name,
            file_path=str(output_path),
            preview_url=f"/preview/{file_name}",
            created_at=datetime.utcnow(),
            source=source,
        )
